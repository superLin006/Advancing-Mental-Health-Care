import requests
import json


def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """

    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=hKg5lqIu01DH3enpsbxRKChB&client_secret=BR0JlkCh2hwGyvWVGEpbQRHQlJPsc1fy"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def main():
    # 你的长信息放在这里
    user_message = """
请你帮我整理归纳总结以下内容，适当调整内容，去除冗余部分，要求内容逻辑清晰，语言表达流畅，并且符合实际的医疗建议：
"1病情分析：您好，根据您的描述很有可能是患有抑郁症，建议您到正规医院进一步确诊。抑郁的症状主要有情绪低落或悲观，对生活的兴趣和愉快感下降，精神疲惫，记忆力下降，语言或行动迟缓，自我评价或价值感下降，睡眠障碍等。意见建议：建议在平时的生活中多参加一些朋友的聚会以及健康的运动，简化自己的生活方式，"
"不要喝茶、咖啡等饮料，也不要食用刺激性强的食物，多食用含钙比较丰富的食物，比如牛奶、鱼、虾、红枣、柿子、韭菜、芹菜、蒜苗等。抑郁时多参加一些文娱活动比如郊游、唱歌;跳舞、游泳等，每天坚持半小时左右，持之以恒，可以有效地舒解抑郁情绪。",
"2 问题分析：您好，您心情每次晚上低落，失眠考虑是神经衰弱，与植物神经功能紊乱有关系的，指导建议：建议你口服谷维素、刺五加、B1片来调理。平时生活规律一点，不能熬夜上火的。",
"3抑郁症是神经症的一种，是一种心境障碍！以情感低落、兴趣减退、思维迟缓、以及言语动作减少。抑郁症有三大主要症状，就是情绪低落、思维迟缓和运动抑制。多种抗抑郁药物、物理治疗（如镇痛安眠枕）、心理治疗都可以治疗抑郁症。"
"4指导意见：治疗抑郁强迫症目前常采用认知行为治疗、心理治疗及抗焦虑、抗抑郁药物治疗。医生与患者采用共同分析探讨、自我心理解放、自我松绑、挖掘潜能的方法，找出干预措施，大部分人可获得一定程度的好转。",
"5首先你要相信自己可以治愈自己的问题。不吃药不靠医生。其实抑郁、焦虑都不是病，只是一种坏习惯而已。指导意见一种缺乏安全感的坏习惯。你要让自己自信起来。想想曾经何时做了什么让你有那种自信的感觉，记得那种感觉，要常常保持那种感觉。慢慢的，你就会改掉你的坏习惯。一定要相信自己，相信生活。"
"6 病情分析：口干这症状多是胃火，主要是由于不良饮食生活习惯导致的。建议吃清胃黄连片中药调理，同时采取中医刮痧疗法，意见建议：多喝水，积极参加体  育锻炼，多吃蔬菜水果，禁止进食辛辣刺激性食物，不要吸烟饮酒。"
    """

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": user_message  # 注入长信息
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    main()
