import scrapy
import re


class JcdbSpider(scrapy.Spider):
    name = 'jcdb'
    start_urls = [
        'https://www.japanese-cinema-db.jp/'
    ]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={},
            callback=self.after_submit
        )

    def after_submit(self, response):
        hrefs = list(filter(lambda x: '/Details?id=' in x,
                            response.css('td a::attr(href)').getall()))

        for href in hrefs:
            yield response.follow(href, callback=self.parse_details)

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.after_submit)

    def parse_details(self, response):
        details = response.css('div#detail')

        title = details.css('h3::text').get().strip()
        title_katakana = details.css('h3 span::text').get().strip()

        list_l_dd = details.css('div.moviedetail-listL dd')
        list_r_dd = details.css('div.moviedetail-listR dd')
        category = list_l_dd[0].css('a::text').get().strip()
        release_date = list_l_dd[1].css('dd::text').get().strip()
        production_companies = [item.strip()
                                for item in list_l_dd[2].css('a::text').getall()]
        distributing_agencies = [item.strip()
                                 for item in list_l_dd[3].css('a::text').getall()]
        rating = list_r_dd[0].css('dd::text').get().strip()
        title_en = list_r_dd[1].css('dd::text').get().strip()
        screening_time = list_r_dd[2].css('dd::text').get().strip()

        description = details.css('p.clear::text').get().strip()

        actors = []
        for li in details.css('ul#actor li'):
            role = li.css('li::text').get().strip()
            name = li.css('a::text').get().strip()
            actors.append({"名前": name, "役割": role})

        staffs = []
        staff_dt = details.css('dl#staff').css('dt')
        staff_dd = details.css('dl#staff').css('dd')
        for (dt, dd) in zip(staff_dt, staff_dd):
            occupation = dt.css('dt::text').get().strip()
            for name in [item.strip() for item in dd.css('a::text').getall()]:
                staffs.append({"名前": name, "職種": occupation})

        story = details.css('div.contentsbox2 p::text').getall()[1].strip()

        spec = [re.sub(r'\s+', '', item.strip())
                for item in details.css('ul#spec li::text').getall()]

        other = [re.sub(r'\s+', '', item.strip())
                 for item in details.css('ul#other li::text').getall()]
        other[4] = '国立映画アーカイブ所蔵有無' + other[4]

        data = {
            "id": response.url.replace('https://www.japanese-cinema-db.jp/Details?id=', ''),
            "タイトル": title,
            "カタカナタイトル": title_katakana,
            "英語タイトル": title_en,
            "カテゴリー": category,
            "レーティング": rating,
            "公開年月日": release_date,
            "制作会社": production_companies,
            "配給会社": distributing_agencies,
            "上映時間": screening_time,
            "スタッフ": staffs,
            "出演者": actors,
            "説明": description,
            "ストーリー": story,
            "仕様": spec,
            "その他": other
        }

        yield data
