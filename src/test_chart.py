import pandas as pd
import altair as alt
import data_processing

print("="*60)
print("測試 Altair 圖表")
print("="*60)

# 載入資料
df = data_processing.load_data()
print(f"\n✅ 總共 {len(df)} 筆資料")

# 檢查關鍵欄位
print(f"\n📊 Gen_health_state 的前 5 個值:")
print(df['Gen_health_state'].value_counts().head())

print(f"\n💰 Total_income 的前 5 個值:")
print(df['Total_income'].value_counts().head())

# 建立測試用的聚合資料
print("\n🔄 建立聚合資料...")
test_data = df.groupby(['Gen_health_state', 'Total_income']).size().reset_index(name='count')
print(f"聚合後有 {len(test_data)} 筆資料")
print("\n前 10 筆資料:")
print(test_data.head(10))

# 建立簡單的 Altair 圖表
print("\n📈 建立 Altair 圖表...")
try:
    chart = alt.Chart(test_data).mark_bar().encode(
        x=alt.X('Gen_health_state:N', title='Health State'),
        y=alt.Y('count:Q', title='Count'),
        color=alt.Color('Total_income:N', title='Income Level')
    ).properties(
        width=700,
        height=400,
        title='Test Chart: Health by Income'
    )
    
    # 儲存成 HTML
    chart.save('test_chart.html')
    print("✅ 圖表已儲存到 src/test_chart.html")
    print("請用瀏覽器打開這個檔案查看圖表")
    
    # 也輸出 dict 格式（這是 Dash 使用的格式）
    chart_dict = chart.to_dict()
    print(f"\n圖表 dict 有 {len(chart_dict)} 個 keys:")
    print(list(chart_dict.keys()))
    
except Exception as e:
    print(f"❌ 建立圖表時發生錯誤: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)