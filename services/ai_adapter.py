"""
ContentHub AI平台适配服务
生成各平台专属的文案、标题、标签
"""
import os
import logging
import random
from typing import List, Dict, Any, Optional

import config

logger = logging.getLogger(__name__)


class AIAdapterService:
    """AI平台适配服务类"""

    # 平台风格配置
    PLATFORM_STYLES = {
        "xiaohongshu": {
            "tone": "亲切、生活化、种草属性",
            "emoji_usage": "高",
            "hashtag_style": "#话题#话题",
            "content_length": "中等 (300-500字)",
            "key_features": ["情感共鸣", "实用干货", "真实分享"]
        },
        "douyin": {
            "tone": "活力、创意、节奏感",
            "emoji_usage": "极高",
            "hashtag_style": "##话题",
            "content_length": "短 (50-150字)",
            "key_features": ["爆点前置", "悬念铺垫", "行动号召"]
        },
        "wechat": {
            "tone": "专业、深度、有价值",
            "emoji_usage": "低",
            "hashtag_style": "无",
            "content_length": "长 (800-2000字)",
            "key_features": ["专业分析", "深度解读", "行业洞察"]
        },
        "website": {
            "tone": "正式、品牌感、SEO友好",
            "emoji_usage": "中",
            "hashtag_style": "无",
            "content_length": "中等 (500-1000字)",
            "key_features": ["关键词优化", "结构清晰", "品牌调性"]
        }
    }

    # 通用标签库
    TAG_LIBRARIES = {
        "xiaohongshu": [
            "生活分享", "种草笔记", "好物推荐", "日常穿搭", "美妆心得",
            "探店打卡", "美食分享", "旅行记录", "职场干货", "自我提升",
            "摄影技巧", "家居布置", "母婴好物", "健身打卡", "读书分享"
        ],
        "douyin": [
            "热门", "推荐", "必看", "收藏", "涨知识", "创意", "搞笑",
            "感动", "惊艳", "种草", "好物", "教程", "干货", "神器", "绝了"
        ],
        "wechat": [
            "深度好文", "行业洞察", "专业解读", "案例分析", "趋势预测",
            "专家观点", "数据报告", "解决方案", "经验分享", "实战技巧"
        ],
        "website": [
            "新闻动态", "产品发布", "技术博客", "案例展示", "关于我们",
            "服务介绍", "行业资讯", "企业新闻", "媒体报道", "合作伙伴"
        ]
    }

    # 标题模板库
    TITLE_TEMPLATES = {
        "xiaohongshu": [
            "绝绝子！这个{topic}太赞了",
            "私藏已久的{topic}分享",
            "{topic}的正确打开方式",
            "建议收藏！{topic}全攻略",
            "没人会拒绝的{topic}",
            "挖到宝了！这个{topic}绝了",
            "答应我一定要试试的{topic}",
            "后悔没早点知道的{topic}"
        ],
        "douyin": [
            "{topic}还能这么玩？",
            "绝了！{topic}太牛了",
            "{topic}看到这个算你赚到了",
            "没想到{topic}竟然",
            "{topic}的正确姿势",
            "学会这招{topic}再也不慌",
            "{topic}天花板",
            "被问爆的{topic}"
        ],
        "wechat": [
            "{topic}深度解析：趋势、机遇与挑战",
            "一文读懂{topic}的核心逻辑",
            "{topic}全面指南（2024珍藏版）",
            "关于{topic}，你需要知道的10件事",
            "深度复盘：{topic}的底层规律",
            "从0到1：{topic}实战手册"
        ],
        "website": [
            "{topic} - 官方网站",
            "了解{topic} | 官方产品介绍",
            "{topic}案例与解决方案",
            "关于{topic} - 企业介绍",
            "{topic}新闻动态"
        ]
    }

    def __init__(self):
        self.api_key = config.AI_API_KEY
        self.enabled = bool(self.api_key)

    def generate_content(self, title: str, content: str, platform: str) -> str:
        """
        生成平台专属文案

        Args:
            title: 原始标题
            content: 原始内容
            platform: 目标平台

        Returns:
            str: 平台适配后的文案
        """
        if platform not in self.PLATFORM_STYLES:
            logger.error(f"不支持的平台: {platform}")
            return content

        style = self.PLATFORM_STYLES[platform]

        try:
            if self.enabled:
                # 使用真实AI API
                return self._generate_by_ai(title, content, platform, style)
            else:
                # 模拟生成
                return self._generate_mock(title, content, platform, style)

        except Exception as e:
            logger.error(f"文案生成失败: {e}")
            return content

    def _generate_by_ai(self, title: str, content: str, platform: str, style: Dict) -> str:
        """
        使用AI API生成文案

        Args:
            title: 原始标题
            content: 原始内容
            platform: 目标平台
            style: 平台风格配置

        Returns:
            str: AI生成的文案
        """
        try:
            import requests

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            prompt = f"""请将以下内容改编为适合{style['tone']}风格的内容：
            平台特点：{', '.join(style['key_features'])}
            内容长度：{style['content_length']}
            Emoji使用：{style['emoji_usage']}

            原始标题：{title}
            原始内容：{content}

            请直接输出改编后的文案，不要添加任何说明。"""

            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000,
                "temperature": 0.7
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                logger.error(f"AI API 错误: {response.status_code} - {response.text}")
                return self._generate_mock(title, content, platform, style)

        except Exception as e:
            logger.error(f"AI API 调用失败: {e}")
            return self._generate_mock(title, content, platform, style)

    def _generate_mock(self, title: str, content: str, platform: str, style: Dict) -> str:
        """
        模拟生成文案（当API不可用时）

        Args:
            title: 原始标题
            content: 原始内容
            platform: 目标平台
            style: 平台风格配置

        Returns:
            str: 模拟生成的文案
        """
        emoji_map = {
            "xiaohongshu": "✨🌸💕",
            "douyin": "🔥💯👏",
            "wechat": "",
            "website": ""
        }

        emojis = emoji_map.get(platform, "")

        if platform == "xiaohongshu":
            return f"""{emojis} {title} {emojis}

{content}

{self._get_xiaohongshu_footer()}"""

        elif platform == "douyin":
            return f"""{emojis} {title} {emojis}

{content[:100]}...

👇点击查看更多内容

#热门 #推荐 #种草"""

        elif platform == "wechat":
            return f"""{title}

{content}

---
本文首发于 ContentHub
转载需授权"""

        else:  # website
            return f"""<h1>{title}</h1>

<p>{content}</p>

<div class="meta">来源: ContentHub</div>"""

    def _get_xiaohongshu_footer(self) -> str:
        """获取小红书风格的结尾"""
        footers = [
            "\n\n💡 今天的分享就到这里啦～\n喜欢的话记得点个赞和收藏哦！\n有什么问题评论区见～",
            "\n\n🌟 希望对你们有帮助！\n有问题可以私信我～\n点个关注不迷路！",
            "\n\n✨ 以上就是今天的分享！\n觉得有用就收藏吧～\n评论区告诉我你们还想看什么！"
        ]
        return random.choice(footers)

    def generate_tags(self, platform: str, count: int = 5) -> List[str]:
        """
        生成平台专属标签

        Args:
            platform: 目标平台
            count: 标签数量

        Returns:
            List[str]: 标签列表
        """
        if platform not in self.TAG_LIBRARIES:
            logger.error(f"不支持的平台: {platform}")
            return []

        library = self.TAG_LIBRARIES[platform]

        if len(library) <= count:
            return library.copy()

        return random.sample(library, count)

    def generate_title(self, original: str, platform: str) -> str:
        """
        生成平台专属标题

        Args:
            original: 原始标题
            platform: 目标平台

        Returns:
            str: 平台适配后的标题
        """
        if platform not in self.TITLE_TEMPLATES:
            logger.error(f"不支持的平台: {platform}")
            return original

        templates = self.TITLE_TEMPLATES[platform]
        template = random.choice(templates)

        # 提取关键词
        words = original.replace("的", " ").replace("是", " ").split()
        topic = words[0] if words else "好物"

        return template.format(topic=topic)

    def get_platform_style(self, platform: str) -> Optional[Dict[str, Any]]:
        """
        获取平台风格配置

        Args:
            platform: 平台名称

        Returns:
            Dict: 平台风格配置，无效返回 None
        """
        return self.PLATFORM_STYLES.get(platform)


# 全局服务实例
ai_service = AIAdapterService()
