from django.shortcuts import render
import plotly.graph_objs as go

def candlestick_chart(request):
    # 這裡假設您已經從數據庫中獲取了蠟燭圖數據
    # 用您的實際數據替換下面的示例數據

    # 示例蠟燭圖數據
    data = [
        {'timestamp': '2024-05-01 00:00:00', 'open': 100, 'high': 120, 'low': 90, 'close': 110},
        {'timestamp': '2024-05-01 01:00:00', 'open': 110, 'high': 130, 'low': 100, 'close': 120},
        # 其他蠟燭數據...
    ]

    # 將數據轉換為Plotly所需的格式
    candlestick_data = go.Candlestick(
        x=[entry['timestamp'] for entry in data],
        open=[entry['open'] for entry in data],
        high=[entry['high'] for entry in data],
        low=[entry['low'] for entry in data],
        close=[entry['close'] for entry in data],
        name='Candlestick'
    )

    # 創建圖表佈局
    layout = go.Layout(
        title='Candlestick Chart',
        xaxis=dict(title='Timestamp'),
        yaxis=dict(title='Price')
    )

    # 創建圖表
    fig = go.Figure(data=[candlestick_data], layout=layout)

    # 將圖表轉換為HTML字符串
    plot_div = fig.to_html(full_html=False)

    # 傳遞圖表HTML到模板中
    return render(request, 'candlestick_chart.html', {'plot_div': plot_div})
