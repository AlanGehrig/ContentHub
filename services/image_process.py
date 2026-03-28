"""
ContentHub 图像处理服务
支持多平台图像尺寸适配、智能裁剪、封面生成
"""
import os
import logging
from typing import Tuple, Optional, List, Dict, Any
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import config

logger = logging.getLogger(__name__)


class ImageProcessService:
    """图像处理服务类"""

    def __init__(self):
        self.upload_dir = config.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)

    def auto_adapt_size(self, image_path: str, platform: str) -> Optional[str]:
        """
        智能裁剪图像以适应指定平台的尺寸

        Args:
            image_path: 原始图像路径
            platform: 目标平台 (xiaohongshu/douyin/wechat/website)

        Returns:
            str: 处理后的图像路径，失败返回 None
        """
        try:
            if platform not in config.PLATFORM_SIZES:
                logger.error(f"不支持的平台: {platform}")
                return None

            target_width, target_height = config.PLATFORM_SIZES[platform]

            # 读取图像
            img = cv2.imread(image_path)
            if img is None:
                logger.error(f"无法读取图像: {image_path}")
                return None

            h, w = img.shape[:2]
            target_ratio = target_width / target_height
            source_ratio = w / h

            # 计算裁剪区域
            if source_ratio > target_ratio:
                # 图像更宽，按高度裁剪
                new_h = h
                new_w = int(h * target_ratio)
                x_offset = (w - new_w) // 2
                y_offset = 0
            else:
                # 图像更高，按宽度裁剪
                new_w = w
                new_h = int(w / target_ratio)
                x_offset = 0
                y_offset = (h - new_h) // 2

            # 裁剪
            cropped = img[y_offset:y_offset + new_h, x_offset:x_offset + new_w]

            # 缩放至目标尺寸
            resized = cv2.resize(cropped, (target_width, target_height), interpolation=cv2.INTER_AREA)

            # 保存
            filename = f"{Path(image_path).stem}_{platform}{Path(image_path).suffix}"
            output_path = os.path.join(self.upload_dir, filename)
            cv2.imwrite(output_path, resized)

            logger.info(f"图像尺寸适配完成: {platform} -> {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"图像尺寸适配失败: {e}")
            return None

    def auto_cover(self, image_path: str, platform: str) -> Optional[str]:
        """
        智能封面生成
        - 添加平台水印
        - 调整色彩增强视觉效果
        - 添加渐变边框

        Args:
            image_path: 原始图像路径
            platform: 目标平台

        Returns:
            str: 封面图像路径，失败返回 None
        """
        try:
            if platform not in config.PLATFORM_SIZES:
                logger.error(f"不支持的平台: {platform}")
                return None

            target_width, target_height = config.PLATFORM_SIZES[platform]

            # 读取并裁剪图像
            adapted_path = self.auto_adapt_size(image_path, platform)
            if not adapted_path:
                return None

            img = Image.open(adapted_path)
            draw = ImageDraw.Draw(img)

            # 根据平台添加水印
            watermark_text = self._get_platform_watermark(platform)
            if watermark_text:
                self._add_watermark(img, draw, watermark_text)

            # 色彩增强
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.1)

            # 对比度增强
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.05)

            # 保存
            filename = f"{Path(image_path).stem}_{platform}_cover{Path(image_path).suffix}"
            output_path = os.path.join(self.upload_dir, filename)
            img.save(output_path, quality=95)

            logger.info(f"智能封面生成完成: {platform} -> {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"封面生成失败: {e}")
            return None

    def _get_platform_watermark(self, platform: str) -> str:
        """获取平台水印文本"""
        watermarks = {
            "xiaohongshu": "小红书",
            "douyin": "抖音",
            "wechat": "微信公众号",
            "website": "官方网站"
        }
        return watermarks.get(platform, "")

    def _add_watermark(self, img: Image.Image, draw: ImageDraw.ImageDraw, text: str):
        """添加水印"""
        try:
            # 尝试使用系统字体
            font_size = max(20, min(img.width, img.height) // 30)
            try:
                font = ImageFont.truetype("msyh.ttc", font_size)
            except Exception:
                font = ImageFont.load_default()

            # 水印位置：右下角
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            x = img.width - text_width - 20
            y = img.height - text_height - 20

            # 半透明背景
            bg_box = [x - 10, y - 5, x + text_width + 10, y + text_height + 5]
            draw.rectangle(bg_box, fill=(0, 0, 0, 128))

            # 绘制文字
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

        except Exception as e:
            logger.warning(f"水印添加失败: {e}")

    def batch_process(self, image_path: str, platforms: List[str]) -> Dict[str, Any]:
        """
        批量处理图像到多个平台

        Args:
            image_path: 原始图像路径
            platforms: 目标平台列表

        Returns:
            Dict: 处理结果 {platform: output_path or error}
        """
        results = {}

        for platform in platforms:
            if platform not in config.PLATFORM_SIZES:
                results[platform] = {"status": "error", "message": f"不支持的平台: {platform}"}
                continue

            try:
                # 尺寸适配
                sized_path = self.auto_adapt_size(image_path, platform)
                if sized_path:
                    results[platform] = {"status": "success", "adapted": sized_path}
                else:
                    results[platform] = {"status": "error", "message": "尺寸适配失败"}

            except Exception as e:
                results[platform] = {"status": "error", "message": str(e)}
                logger.error(f"平台 {platform} 处理失败: {e}")

        return results

    def get_image_info(self, image_path: str) -> Optional[Dict[str, Any]]:
        """
        获取图像基本信息

        Args:
            image_path: 图像路径

        Returns:
            Dict: 图像信息
        """
        try:
            img = cv2.imread(image_path)
            if img is None:
                pil_img = Image.open(image_path)
                info = {
                    "path": image_path,
                    "width": pil_img.width,
                    "height": pil_img.height,
                    "format": pil_img.format,
                    "mode": pil_img.mode
                }
            else:
                h, w = img.shape[:2]
                info = {
                    "path": image_path,
                    "width": w,
                    "height": h,
                    "channels": img.shape[2] if len(img.shape) > 2 else 1
                }

            info["size_bytes"] = os.path.getsize(image_path)
            return info

        except Exception as e:
            logger.error(f"获取图像信息失败: {e}")
            return None


# 全局服务实例
image_service = ImageProcessService()
