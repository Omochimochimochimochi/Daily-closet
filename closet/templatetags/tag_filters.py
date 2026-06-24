from django import template

register = template.Library()


@register.filter
def hashtags(value):
    """
    'ストレート,ウェーブ' のようなカンマ区切り文字列を
    '#ストレート #ウェーブ' のような表示用文字列に変換する。
    空文字やNoneの場合は空文字を返す。
    """
    if not value:
        return ""
    tags = [t.strip() for t in value.split(',') if t.strip()]
    return " ".join(f"#{t}" for t in tags)