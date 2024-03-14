import requests
from bs4 import BeautifulSoup


def fetch_data():
    # 发送HTTP请求获取网页内容
    url = "https://resonance.breadio.wiki/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def parse_city_data(soup):
    city_data = []
    city_divs = soup.select(".rounded-lg")
    for div in city_divs:
        city_name = div.find('h3').text.strip()
        table = div.find('table')
        # 解析表格数据,提取商品信息
        local_products, other_cities_products = parse_table_data(table)
        city_data.append({
            'city_name': city_name,
            'local_products': local_products,
            'other_cities_products': other_cities_products
        })
    return city_data


def parse_table_data(table):
    local_products = []
    other_cities_products = {}

    # 遍历表格行,提取商品信息
    rows = table.find_all('tr')
    header_cols = rows[0].find_all('th')[2:]
    city_names = [col.text.strip() for col in header_cols]

    for row in rows[1:]:
        cols = row.find_all('td')
        if cols:
            product_name = cols[0].find('a').text.strip() if cols[0].find('a') else None
            local_price_increase = extract_local_city_diff(cols[1])

            if product_name:
                local_products.append({
                    'name': product_name,
                    'increase': local_price_increase,
                })

                other_cities_products[product_name] = []
                for index, col in enumerate(cols[2:], start=2):
                    price_increase = extract_other_city_diff(col)
                    price = extract_other_city_price(col)
                    if price_increase != 0:
                        other_city_name = city_names[index - 2]
                        other_cities_products[product_name].append({
                            'city_name': other_city_name,
                            'increase': price_increase,
                            'price': price
                        })

    return local_products, other_cities_products


# 提取本市所卖商品的增幅
def extract_local_city_diff(col) -> int:
    price_info_div = col.find('div', class_='h-6 flex gap-1 items-center')
    if price_info_div:
        price_increase_tag = price_info_div.find('span', class_='text-red')
        if price_increase_tag:
            price_increase_str = price_increase_tag.text.strip()
            if price_increase_str and price_increase_str[:-1].isdigit():
                price_increase_int = int(price_increase_str[:-1])  # 去掉百分号,并转换为整数
                return price_increase_int
    return 0


def extract_other_city_diff(col) -> int:
    price_info_div = col.find_all('div', class_='h-6 flex gap-1 items-center')
    if price_info_div and len(price_info_div) > 1:
        price_increase_tag = price_info_div[1].find('span', class_='text-green')
        if price_increase_tag:
            price_increase_str = price_increase_tag.text.strip()
            if price_increase_str and price_increase_str[:-1].isdigit():
                price_increase_int = int(price_increase_str[:-1])  # 去掉百分号,并转换为整数
                return price_increase_int
    return 0


def extract_other_city_price(col) -> int:
    price_info_div = col.find_all('div', class_='h-6 flex gap-1 items-center')
    if price_info_div and len(price_info_div) > 1:
        price_tag = price_info_div[0].find_all('span')[1]
        if price_tag:
            price = price_tag.text.strip()
            return price
    return 0


def find_best_deals(city_data):
    best_deals = []

    for city in city_data:
        city_name = city['city_name']
        local_products = city['local_products']
        other_cities_products = city['other_cities_products']

        for product in local_products:
            product_name = product['name']
            local_increase = product['increase']

            if product_name in other_cities_products:
                for other_city_product in other_cities_products[product_name]:
                    other_city_name = other_city_product['city_name']
                    other_city_increase = other_city_product['increase']
                    other_city_price = other_city_product['price']
                    if local_increase == 0 or other_city_increase == 0:
                        continue

                    if other_city_increase - local_increase > 30:
                        best_deals.append({
                            '商品名': product_name,
                            '本地城市': city_name,
                            '目标城市': other_city_name,
                            '标价': other_city_price,
                            '增幅结果': other_city_increase - local_increase
                        })

    return best_deals

def main():
    soup = fetch_data()
    city_data = parse_city_data(soup)
    best_deals = find_best_deals(city_data)

    # 按照增幅降序排序
    sorted_best_deals = sorted(best_deals, key=lambda deal: deal['增幅结果'], reverse=True)

    print("雷索纳斯市场检测工具")
    print("================================")

    # 打印符合条件的increase值
    for city in city_data:
        if city['city_name'] == '淘金乐园':
            for product in city['local_products']:
                if product['name'] == '沙金':
                    if product['increase'] == 0:
                        print("沙金目前没有合适的买点")
                    else:
                        print(f"沙金目前市场行情价: {product['increase']}")

    print("================================")

    # 修改打印纯金线材在其他城市的增幅，使其一行打印
    for city in city_data:
        if '纯金线材' in city['other_cities_products']:
            print("纯金线材在其他城市的增幅:")
            for other_city_product in city['other_cities_products']['纯金线材']:
                print(f"{other_city_product['city_name']}: {other_city_product['increase']}%, ", end='')
            print()  # 添加换行符，在所有城市增幅输出后换行

    print("================================")

    # 输出最优商品倒卖方案，每一列对齐显示
    print("最优商品倒卖方案:")
    for deal in sorted_best_deals[:3]:
        print(f"商品名: {deal['商品名']:<15} | 出发城市: {deal['本地城市']:<10} | 到达城市: {deal['目标城市']:<10} | 标价: {deal['标价']:<10} | "
              f"增幅结果: {deal['增幅结果']:.2f}%")

    print("================================")

if __name__ == '__main__':
    main()

#
# 修格里城，铁盟哨站，7号自由港，澄明数据中心，阿妮塔战备工厂，阿妮塔能源研究所，荒原站，曼德矿场，淘金乐园
#
# 阿妮塔能源研究所 -> 300 -> 阿妮塔战备工厂
# 阿妮塔能源研究所 -> 400 -> 7号自由港 -> 600 ->澄明数据中心 -> 300 -> 修格里城 -> 200 -> 铁盟哨站 -> 200 -> 荒原站 -> 200 -> 曼德矿场 -> 300 -> 淘金乐园
