import requests

# 假设直播源提供了一个API来检查回看功能
def check_live_replay(live_url):
    # 这里假设API的URL是 live_url + '/api/check_replay'
    api_url = live_url + '/api/check_replay'
    
    # 发起请求
    response = requests.get(api_url)
    
    # 检查响应状态码
    if response.status_code == 200:
        # 解析返回的数据
        data = response.json()
        
        # 假设返回的数据中有一个字段叫做 'replay_supported' 来表示是否支持回看
        if data.get('replay_supported'):
            print("该直播源支持回看。")
            # 这里可以进一步处理回看的信息，如获取回看的URL等
        else:
            print("该直播源不支持回看。")
    else:
        print("请求失败，无法检查直播源的回看功能。")

# 示例直播源URL
live_url_example = 'http://example.com/live'
check_live_replay(live_url_example)
