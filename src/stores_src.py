# Source of truth for the map data. Run: python3 -I stores_src.py  -> stores.json
# y0q: e = exact year, a = approximate, b = "by": first seen in a source of that year (opened on or before)
# y1: None = still open; y1q: e exact, a approximate, u = last seen in a source that year (fate unknown)
import json, os

SOURCES = [
    ("換日線／Smile Taiwan：台北特色唱片行", "https://smiletaiwan.cw.com.tw/article/9455"),                     # 0
    ("遠見：全台最大黑膠唱片行（大韜黑膠北流店）, 2024", "https://www.gvm.com.tw/article/109622"),                # 1
    ("鏡週刊：上揚唱片, 2025", "https://www.mirrormedia.mg/story/amp/20251119bus001"),                          # 2
    ("Marie Claire：黑膠唱片行推薦, 2025", "https://www.marieclaire.com.tw/lifestyle/news/84182"),               # 3
    ("HiveLife: Vinyl stores in Taipei, 2021", "https://hivelife.com/vinyl-stores-in-taipei"),                 # 4
    ("Music Photo Life: Vinyl record shopping in Taipei, 2024", "https://musicphotolife.com/2024/04/vinyl-record-shopping-taipei/"),  # 5
    ("Taiwan Scene: Analog sounds in digital times, 2020", "https://taiwan-scene.com/analog-sounds-digital-times-dedicated-record-stores-in-taipei/"),  # 6
    ("Nivessa: Record stores in Taipei（店家名錄）", "https://nivessa.com/record-stores/taiwan/taipei-city/taipei"),  # 7
    ("Mixmag Asia: 9 DJs spill secret spots, 2017", "https://mixmag.asia/feature/9-djs-spill-secret-spots-to-go-crate-digging-asia"),  # 8
    ("維基百科：淘兒唱片", "https://zh.wikipedia.org/zh-tw/%E6%B7%98%E5%85%92%E5%94%B1%E7%89%87"),               # 9
    ("風傳媒：連鎖唱片行全面熄燈, 2026", "https://www.storm.mg/lifestyle/11179302"),                             # 10
    ("Sai：台北唱片行漫步（持續更新）, 2022–2026", "https://santora.tw/record-stores-in-taipei/"),               # 11
    ("2019 台北實體影音 CD/DVD/BD 專賣店 Part.1", "https://minazukiw.pixnet.net/blog/posts/46788644"),          # 12
    ("2019 台北實體影音 CD/DVD/BD 專賣店 Part.2", "https://minazukiw.pixnet.net/blog/posts/46803928"),          # 13
    ("2019 台北實體影音 CD/DVD/BD 專賣店 Part.3 公館", "https://minazukiw.pixnet.net/blog/posts/46842068"),    # 14
    ("維基百科：玫瑰大眾唱片", "https://zh.wikipedia.org/zh-tw/%E7%8E%AB%E7%91%B0%E5%A4%A7%E7%9C%BE%E5%94%B1%E7%89%87"),  # 15
    ("CTWANT：最後一家玫瑰大眾唱片行熄燈, 2026", "https://www.ctwant.com/amp/article/505460/"),                  # 16
    ("Bitetone 論壇：台灣唱片店列表, 2013／2017", "https://bitetone.com/forums/topic/%E5%8F%B0%E7%81%A3%E5%94%B1%E7%89%87%E5%BA%97%E5%88%97%E8%A1%A8/"),  # 17
    ("五大唱片：門市資訊", "https://www.5music.com.tw/store.asp"),                                              # 18
    ("VERSE：全台 Top 10 樂迷必訪唱片行, 2024", "https://www.verse.com.tw/article/10-record-store"),            # 19
    ("Taiwan Scene: The renaissance of music, 2022", "https://taiwan-scene.com/2022/12/14/the-renaissance-of-music-a-revival-of-cds-and-cassettes/"),  # 20
    ("Hypebeast：摔碟唱片舍, 2025", "https://hypebeast.com/zh/2025/8/slipped-disk-info"),                       # 21
    ("TRAVELER Luxe：THT 黑膠音樂圖書館開幕, 2024", "https://www.travelerluxe.com/article/desc/240010625"),      # 22
    ("Pinkoi：精選 4 間台北復古唱片行, 2022", "https://blog.pinkoi.com/tw/hot-topics/art-design/2112-record-stores/"),  # 23
    ("鏡週刊：誠品敦南店熄燈, 2020", "https://www.mirrormedia.mg/story/20200531edi004"),                        # 24
    ("數位時代：哈囉 光華數位新天地", "https://www.bnext.com.tw/article/796/BN-ARTICLE-796"),                    # 25
    ("AVC Coffee Roasters 黑膠咖啡廳介紹, 2026", "https://upssmile.com/279469/avc-coffee-roasters"),            # 26
    ("維基百科：小白兔唱片", "https://zh.wikipedia.org/zh-tw/%E5%B0%8F%E7%99%BD%E5%85%94%E5%94%B1%E7%89%87"),     # 27
    ("Readmoo 閱讀最前線：小白兔唱片, 2018", "https://news.readmoo.com/2018/05/25/180525-white-rabbit/"),       # 28
    ("P Paper：Waiting Room, 2024", "https://ppaper.net/1648/"),                                               # 29
    ("Blow 吹音樂：風和日麗唱片行熄燈", "https://blow.streetvoice.com/46696/"),                                  # 30
    ("M@M Records：關於我們", "https://www.mmrecords.com.tw/pages/mm-records-taipei-taiwan"),                   # 31
    ("新頭殼 xinmedia：沒有新歌的唱片行, 2014", "https://www.xinmedia.com/article/14960"),                       # 32
    ("Digging Movement：2manyminds Records, 2016", "https://diggingmovement.blogspot.com/2016/09/201682699-2manyminds-records.html"),  # 33
    ("PUWU Life：BEANS & BEATS, 2015", "https://puwulife.com/2015-03-08-573/"),                               # 34
    ("Blow 吹音樂：摔碟唱片舍, 2025", "https://blow.streetvoice.com/82236/"),                                    # 35
    ("自由時報：誠品音樂館與敦南店, 2020", "https://ec.ltn.com.tw/article/breakingnews/3099551"),                  # 36
    ("中央社：誠品信義店熄燈, 2023", "https://www.cna.com.tw/news/acul/202312230220.aspx"),                       # 37
    ("1010 online：黑膠咖啡 Vinyl Decision", "https://www.1010online.com.tw/journal/phonograph-record-cafe"),  # 38
    ("YSOLIFE：小宋唱片, 2019", "https://www.ysolife.com/song-record/"),                                       # 39
    ("Fliper：THT 搬家, 2024", "https://flipermag.com/2024/07/23/this-hidden-track/"),                        # 40
    ("文化部 文化幣：唱片行店家名單（2026 查詢）", "https://twcp.moc.gov.tw/prec-u/culturePoints/search?role=122&city=ALL&area=null&cityName=%E5%85%A8%E9%81%B8&currentPage=1&pageSize=8"),  # 41
    ("Record Store Day Taiwan 2026 參與店家", "https://www.recordstoreday.tw/stores"),                          # 42
    ("Cassette Store Day Taiwan 2023 參與店家", "https://www.cassettestoreday.tw/"),                            # 43
    ("Audionet 論壇：先行一車, 2015", "https://www.audionet.com.tw/thread-7192-1-1.html"),                      # 44
    ("中央社：先行一車, 2018", "https://www.cna.com.tw/culture/article/20180112w006"),                         # 45
    ("Bella 儂儂：聲色 Sounds Good, 2021", "https://www.bella.tw/articles/travel&foodies/32604"),               # 46
    ("聯合報：台北聆聽咖啡廳與酒吧, 2026", "https://udn.com/news/story/6962/9744396"),                          # 47
    ("Tatler Asia：潮電 ChaoBar, 2024", "https://www.tatlerasia.com/gen-t/others/2024-gent-barrecord-store-zh-hant"),  # 48
    ("今周刊：台北唱片行, 2014", "https://www.businesstoday.com.tw/article/category/151139/post/201410230006/"),  # 49
    ("今周刊：獨立唱片行, 2008", "https://www.businesstoday.com.tw/article/category/80732/post/200810160010/"),   # 50
    ("城市學：大浪漫商店, 2022", "https://city.gvm.com.tw/article/89827"),                                     # 51
    ("公視新聞：第一唱片行, 2020", "https://news.pts.org.tw/article/502822"),                                  # 52
    ("數位時代：法雅客來台, 1999", "https://www.bnext.com.tw/article/8905/BN-ARTICLE-8905"),                    # 53
    ("Taipei Times: Taipei's record stores, 2006", "https://www.taipeitimes.com/News/feat/archives/2006/11/10/2003335720"),  # 54
    ("焦元溥（VERSE，LINE TODAY 轉載）：唱片行回憶, 2021", "https://today.line.me/tw/v2/article/0kGg2l"),        # 55
    ("VERSE：羅斯福路上的唱片行", "https://www.verse.com.tw/article/record-roosevelt-road"),                     # 56
    ("羅悅全〈唱片行東西南北中〉，《秘密基地》2000 年 5 月（音謀筆記轉載）", "https://jeph.bluecircus.net/archives/40"),                             # 57
    ("Cynical Audio：大眾唱片台大店將結束, 2012", "http://www.cynicalaudio.com/2012/03/blog-post_18.html"),        # 58
    ("中央社（蕃薯藤轉載）：五大唱片西門店租約訴訟, 2016", "https://n.yam.com/Article/20160102485365"),            # 59
    ("wildflower 部落格：台北車站一帶唱片行, 2007", "https://wildflower.pixnet.net/blog/post/28563859"),          # 60
    ("minazukiw 部落格：佳佳忠孝店改名樂樂唱片, 2014", "https://minazukiw.pixnet.net/blog/posts/41135962"),        # 61
    ("Blow 吹音樂：宇宙城唱片回憶", "https://blow.streetvoice.com/57349/"),                                     # 62
    ("中國時報：玫瑰大眾最後門市熄燈, 2026", "https://www.chinatimes.com/realtimenews/20261105005597-260405"),     # 63
    ("Latte Korea：台北 K-pop 專輯店整理（約 2024）", "https://lattekorea.com/taipei-kpop-album/"),              # 64
    ("鏡週刊：K-MONSTAR 展店, 2025", "https://www.mirrormedia.mg/story/20250206insight005"),                    # 65
    ("「無限期支持實體唱片」粉絲專頁製作的台北唱片行名單，2014 年 5 月 2 日（之後有增修）", "https://www.facebook.com/SupportPhysicalMusic"),                                          # 66
    ("music-xo 部落格：台北唱片行清單, 2014-08", "http://music-xo.blogspot.com/2014/08/blog-post.html"),         # 67
    ("新頭殼 xinmedia：小閔的古典音樂世界熄燈, 2014", "https://www.xinmedia.com/article/15869"),                  # 68
    ("中央社：小閔的古典音樂世界, 2024", "https://www.cna.com.tw/news/acul/202410160048.aspx"),                  # 69
    ("巨禮音響 Cheery Music：關於我們", "https://www.cheerymusic.com/"),                                       # 70
    ("JOY AUDIO：門市資訊", "https://www.joyaudio.com.tw/shop_content.php?coID=9"),                            # 71
    ("韻順股份有限公司登記資料", "https://opengovtw.com/ban/23766532"),                                         # 72
    ("澤龍唱片有限公司登記資料", "https://opengovtw.com/ban/89950989"),                                         # 73
    ("極光唱片：通路門市", "https://www.aurora.ws/store"),                                                     # 74
    ("停看聽音響有限公司登記資料", "https://company.g0v.ronny.tw/api/show/84483557"),                           # 75
    ("HD.Club 論壇：台北影音唱片店整理, 2017–2021", "https://www.hd.club.tw/thread-223926-1-1.html"),           # 76
    ("新頭殼 xinmedia：貳樂號 2manyminds, 2014", "https://www.xinmedia.com/article/15725"),                     # 77
    ("The Funk Soul Spectre：Spykee 訪談, 2019", "https://thefunksoulspectre.wordpress.com/2019/05/31/spykee-pt1/"),  # 78
    ("YSOLIFE：agnès b. music store, 2014", "https://ysolife.com/agnes-b-music-storecloud-nothing/"),          # 79
    ("Marie Claire：agnès b. 微風松高店熄燈, 2020", "https://www.marieclaire.com.tw/fashion/news/50218"),       # 80
    ("VERSE：台灣ê店變身讀派, 2022", "https://www.verse.com.tw/article/bookstore-taiwan-thok-phai"),            # 81
    ("Mangasick 部落格：Seed Toss 結束實體營業, 2015", "http://mangasick.blogspot.com/2015/06/blog-post.html"),  # 82
    ("PTT WesternMusic：樂樂唱片清倉, 2015", "https://www.pttweb.cc/bbs/WesternMusic/M.1436190324.A.0B3"),       # 83
    ("再生工場：關於我們", "https://www.shshop.me/pages/about"),                                                # 84
    ("窩客島：再生工場站前店, 2023", "https://www.walkerland.com.tw/article/view/366769"),                     # 85
    ("五大國際唱片 許昌分公司登記資料", "https://company.g0v.ronny.tw/api/show/24359597"),                     # 86
    ("vocus：五大唱片搬到對面二樓, 2024", "https://vocus.cc/article/663b204bfd897800014431e3"),                # 87
    ("U-Audio：新天新地遷址, 2020", "https://feature.u-audio.com.tw/featuredetail.asp?featureid=1170"),         # 88
    ("新天新地 STSD 官網", "https://www.stsd99.com/"),                                                          # 89
    ("蔡政忠提供：台灣實體唱片行地圖@2020（2020-05-13）", ""),          # 90
    ("大眾唱片官網〈各店位址〉，Wayback Machine 2001–2005 封存", "https://web.archive.org/web/20010608120854/http://www.tcr.com.tw:80/salespoint.asp"),  # 91
    ("G-Music〈關於台灣風雲榜〉：全省大眾玫瑰 47 家門市，2002 封存", "https://web.archive.org/web/20020719040246/http://www.g-music.com.tw:80/about.htm"),  # 92
    ("維基百科：太電欣榮實業（T-ZONE / T-Wave）", "https://zh.wikipedia.org/zh-tw/%E5%A4%AA%E9%9B%BB%E6%AC%A3%E6%A6%AE%E5%AF%A6%E6%A5%AD"),  # 93
    ("東吳大學圖書館館刊：台北唱片行介紹，2004-04", "https://www.lib.scu.edu.tw/pub/s18/18-6.pdf"),             # 94
    ("國家文化記憶庫：1998 年黃子佼開唱片行（中國時報照片）", "https://catalog.digitalarchives.tw/item/00/5c/11/c7.html"),  # 95
    ("台灣好玩：IMPO 唱片, 2002", "https://www.taiwanfun.com/north/taipei/shopping/0204/0204wnIMPOTW.htm"),      # 96
    ("RoxyRocker：IMPO 唱片行楊傑格訪談, 2015", "https://roxyrocker.com/2015/12/22/【roxyrocker-人物訪談】impo-唱片行-楊傑格/"),  # 97
    ("中國時報：誠品 R79 開幕, 2017", "https://www.chinatimes.com/newspapers/20170715000539-260107"),           # 98
    ("華山1914：風潮音樂旗艦店", "https://www.huashan1914.com/w/huashan1914/CustomShops_20060210352905283"),   # 99
    ("維基百科：法雅客", "https://zh.wikipedia.org/zh-tw/%E6%B3%95%E9%9B%85%E5%AE%A2"),                         # 100
    ("越點專業音響：關於我們", "https://acdc.com.tw/about-us/"),                                                # 101
    ("Audionet：停看聽搬到重慶北路, 2017", "https://www.audionet.com.tw/thread-9845-1-1.html"),                 # 102
    ("kuangnan1017 部落格：光南大批發門市清單, 2009", "https://kuangnan1017.pixnet.net/blog/post/25359423"),     # 103
    ("光南大批發：台北公館門市", "https://www.knn.com.tw/%E9%96%80%E5%B8%82%E8%B3%87%E8%A8%8A"),               # 104
    ("看見新聞 knews：玫瑰大眾古典館 2022 年搬到重慶南路", "https://www.knews.com.tw/news/61E4C71DDC14C2C367E5013448EC3449"),  # 105
    ("玫瑰唱片官網〈全省玫瑰通路網〉，2001 年 2–8 月封存", "https://web.archive.org/web/20010203115400/http://www.roserecords.com.tw:80/rose/net.asp"),  # 106
    ("玫瑰唱片官網〈門市〉，2001 年 11 月–2002 年 6 月封存", "https://web.archive.org/web/20020606074556/http://www.roserecords.com.tw:80/welcome/retail.asp"),  # 107
    ("玫瑰唱片官網〈古典館介紹〉（公司沿革），2001 封存", "https://web.archive.org/web/20011230092159/http://www.roserecords.com.tw:80/welcome/class_retail.asp"),  # 108
    ("G-Music〈關於玫瑰〉玫瑰門市表，2005–2016 年封存（每季抽樣）", "https://web.archive.org/web/20051124193236/http://www.g-music.com.tw:80/GMusicAboutRose.aspx"),  # 109
    ("G-Music〈關於大眾〉大眾門市表，2005–2021 年封存（每季抽樣）", "https://web.archive.org/web/20051029062923/http://www.g-music.com.tw:80/GMusicAboutTcr.aspx"),  # 110
    ("PTT V6 板〈[商店情報] 佳佳唱片行〉，2001-12", "https://www.ptt.cc/man/V6/DE2E/D1E9/D210/D5E6/M.1007647469.A.html"),  # 111
    ("YSO Life：唱片行尋寶地圖・佳佳唱片（漢口店 1998 年開設）", "https://ysolife.com/chia-chia-record/"),  # 112
    ("豆瓣：台灣唱片行地圖（佳佳漢口店 2015-04-01 遷至 B1）", "https://www.douban.com/note/481693598/"),  # 113
    ("無非文化・生活精品〈全省門市通訊〉（多為唱片行），2003-04 封存；清單編於 2001-08 至 2003-04 之間", "https://web.archive.org/web/20030417021412/http://www.ebtc.com.tw:80/GIFT/add.html"),  # 114
    ("asodf 部落格轉貼 Yahoo!知識+〈玫瑰唱片的地址?〉，2005-08", "https://asodf.pixnet.net/blog/posts/8119101685"),  # 115
    ("PTT BigShiLin 板：懷念士林消失的店家（元元唱片）", "https://www.ptt.cc/bbs/BigShiLin/M.1637236067.A.B34.html"),  # 116
    ("《音樂時代》月刊〈全省各大暢銷名店索引〉，1996 年（宗山提供）", ""),  # 117
    ("駱克唱片行官網〈關於駱克〉", ""),  # 118
    ("駱克唱片行 2021 年 1 月搬家公告", ""),  # 119
    ("PTT clmusic 板〈[情報] 駱克唱片行的二手CD〉，2007-05-30", "https://www.ptt.cc/bbs/clmusic/M.1180460156.A.23D.html"),  # 120
    ("KEEDAN 起點：微樂客實體門市正式上路，2024-03-07", "https://keedan.com/track/2024/03/07/keedan-scene-willmusic/"),  # 121
    ("老闆娘的店營業期間（製作者 Brien John 提供）", ""),  # 122
    ("製作者 Brien John 提供（2026 年 11 月）：agnès b. music store 營業至 2017 年、三創黑膠 2026 年歇業、KAERU 預計 2026 年底開店、佳佳站前店遷址經過、攝氏三十八度 1989 年設立、第一唱片行 2026 年仍營業", ""),  # 123
    ("KAERU 官方網站（網路商店，聯絡地址與門市自取）", "https://www.kaerutw.com/"),  # 124
    ("Google 地圖：蒙得你安唱片 Mondrian Vinyls（2026 年 11 月查詢）", "https://maps.app.goo.gl/vVseBPLPSg77cg8Y7"),  # 125
    ("PopDaily：台灣 14 間 K-POP 專輯周邊店, 2025", "https://www.popdaily.com.tw/korea/1513994"),  # 126
    ("仙女樹 FAIRYTREE 官網門市資訊", "https://www.fairytree.com.tw/pages/new-page"),  # 127
    ("TVBS 新聞：K-pop 全台實體專輯店, 2025", "https://news.tvbs.com.tw/entertainment/3029319"),  # 128
    ("KEEDAN 起點：中山站周邊 K-POP 專輯店, 2026-05-12（2026-10-29 更新）", "https://keedan.com/track/2026/05/12/zhongshan-kpop-store-guide/"),  # 129
    ("統編速搜：微樂客有限公司各門市部登記資料", "https://site.reurl.tw/details/00605911"),  # 130
    ("聯合新聞網：全台實體專輯店, 2025-10", "https://travel.udn.com/travel/story/7934/9103225"),  # 131
    ("V-EIGHT CORP. 公司沿革（K-MONSTAR 展店年表）", "https://www.v8corp.com/"),  # 132
    ("MOOK 景點家：台北 K-POP 專賣店, 2025-08-27", "https://www.mook.com.tw/article/38533/page/2/"),  # 133
    ("韓居 HGmusic 官網〈商店介紹〉", "https://www.hgmusic.com.tw/zh-TW/pages/about-us-copy"),  # 134
    ("104 人力銀行：ALL MY DAY 經營公司簡介", "https://www.104.com.tw/company/1a2x6bnf05"),  # 135
    ("ALL MY DAY 官網：中山門市開幕活動", "https://allmyday.com.tw/post/%E4%B8%AD%E5%B1%B1%E9%96%80%E5%B8%82%E9%96%8B%E5%B9%95%E6%B4%BB%E5%8B%9568e7fe9de6716"),  # 136
    ("KOREEPOP 官網〈關於我們〉", "https://www.koreepop.com/pages/about-us"),  # 137
    ("中央廣播電台（江昭倫）：三創自設品牌 設全台最大庫藏黑膠店, 2015-05-15", "https://tw.news.yahoo.com/%E4%B8%89%E5%89%B5%E8%87%AA%E8%A8%AD%E5%93%81%E7%89%8C-%E8%A8%AD%E5%85%A8%E5%8F%B0%E6%9C%80%E5%A4%A7%E5%BA%AB%E8%97%8F%E9%BB%91%E8%86%A0%E5%BA%97-042100554.html"),  # 138
    ("PTT Z-Chen 板：智成「店員萬萬歲」答謝唱片行行程（轉貼官網）, 2003-03-13", "https://www.ptt.cc/bbs/Z-Chen/M.1047557456.A.044.html"),  # 139
    ("Impo 唱片 Facebook 粉絲專頁（2026 年 11 月仍有貼文，標示週六、日 13:00–19:00 營業）", "https://www.facebook.com/61567178580798"),  # 140
    ("燭光唱片提供：店址與搬遷經過（2026 年 11 月）", ""),  # 141
    ("啟元唱片 Facebook 粉絲專頁（2026 年 10 月仍有貼文）", "https://www.facebook.com/cdmusic.taipei/"),  # 142
    ("國家兩廳院〈駐店禮品・音樂國度〉，Wayback Machine 2015-10 至 2020-07 封存（列出風潮音樂）", "https://web.archive.org/web/20200705205956/http://npac-ntch.org/zh/stores/page-%E9%9F%B3%E6%A8%82%E5%9C%8B%E5%BA%A6-e71lbmbn5n"),  # 143
    ("國家兩廳院〈風格店鋪〉，2022-12 封存與 2026-11 現況（已無風潮音樂）", "https://npac-ntch.org/visits/stores"),  # 144
    ("Google 地圖：小宋唱片（2026 年 11 月仍列營業時間，店家回覆近期評論）", "https://maps.app.goo.gl/wsA4KnR5B8EpbrhE7"),  # 145
    ("蕭玲玲（前玫瑰唱片副總經理、Tower Records 總經理）提供：〈玫瑰唱片各門市開幕日期一覽表〉，資料更新於 2000-10-17", ""),  # 146
]

ZONES = [
    # n, lat, lng, radius (m), show label, label offset px
    dict(n="西門町", lat=25.0428, lng=121.5068, r=550, label=1, dx=-34, dy=-4),
    dict(n="台北車站", lat=25.0455, lng=121.5140, r=520, label=1, dx=0, dy=-14),
    dict(n="光華・華山", lat=25.0450, lng=121.5300, r=650, label=1, dx=0, dy=-14),
    dict(n="師大・公館", lat=25.0200, lng=121.5310, r=1300, label=1, dx=-14, dy=24),
    dict(n="中山", lat=25.0545, lng=121.5280, r=1300, label=1, dx=0, dy=-16),
    dict(n="東區", lat=25.0420, lng=121.5480, r=900, label=1, dx=0, dy=-14),
    dict(n="信義", lat=25.0380, lng=121.5660, r=900, label=1, dx=0, dy=-14),
    dict(n="松山・民生", lat=25.0580, lng=121.5530, r=1300, label=1, dx=0, dy=-14),
    dict(n="通化・六張犁", lat=25.0260, lng=121.5540, r=900, label=1, dx=0, dy=22),
]

def S(id, n, t, a, y0, y0q, y1, y1q, src, note="", en="", geo=None, zone=None):
    d = dict(id=id, n=n, t=t, a=a, y0=y0, y0q=y0q, y1=y1, y1q=y1q, src=src)
    if note: d["note"] = note
    if en: d["en"] = en
    if geo: d["geo"] = geo
    if zone: d["zone"] = zone
    return d

STORES = [
    # ---- 連鎖通路 ----
    S("tower-east", "淘兒唱片 頂好店（東淘）", "chain", "台北市大安區忠孝東路四段71之1號2樓", 1992, "a", 2003, "a", [9, 10, 57, 117],
      "Tower Records 1992 年進入台灣；2003 年 11 月退出台灣市場。各分店確切開店年不詳。", "Tower Records"),
    S("tower-ximen", "淘兒唱片 西門店（西淘）", "chain", "台北市萬華區成都路12號", 1992, "e", 2003, "a", [9, 10, 16, 57, 117, 139],
      "西門紅樓旁三層樓的金黃色店面，1992 年開幕，2003 年隨淘兒退出台灣結束。", "Tower Records", geo="台北市萬華區成都路10號"),
    S("tower-tianmu", "淘兒唱片 天母店", "chain", "台北市士林區忠誠路二段55號（大葉高島屋4樓）", 1994, "a", 2003, "a", [9],
      "設於大葉高島屋 4 樓，開店年不詳。", "Tower Records", geo="台北市士林區忠誠路二段55號"),
    S("tower-xinyi", "淘兒唱片 信義店", "chain", "台北市信義區松高路12號（新光三越 A8 6樓）", 2003, "b", 2003, "a", [9],
      "設於新光三越信義新天地 A8 館 6 樓，開店年不詳。", "Tower Records", geo="台北市信義區松高路12號"),
    S("rose-gongguan", "玫瑰唱片 公館店（142號）", "chain", "台北市文山區羅斯福路四段142號", 1987, "e", 2001, "e", [146, 10, 15, 55, 57, 106, 107, 117],
      "玫瑰唱片 1987 年 3 月 9 日在公館開出全台第一家門市，2000 年 9 月 1 日改裝重新開幕。玫瑰官網 2001 年 6 月還列出「公館店 1F」在 142 號，8 月起名單上已沒有這個地址。", geo="台北市中正區羅斯福路四段142號"),
    S("rose-ntu", "玫瑰唱片 公館店（羅斯福路 110 號）", "chain", "台北市中正區羅斯福路四段110號1-2樓", 2000, "e", 2007, "e", [146, 106, 107, 10, 15, 109, 114, 139],
      "2000 年 8 月 10 日以「台大店」開幕，2005 年起改稱公館店。142 號老店歇業後，這裡是玫瑰在公館唯一的店。門市表 2007 年 4 月還在、7 月已無，與報導所說 2007 年 3 月「玫瑰公館店」結束相符。"),
    S("rose-music99", "音樂 99（玫瑰體系）", "chain", "台北市中正區汀州路三段194號2樓之1", 2000, "e", 2001, "a", [146, 106],
      "宇宙城原址，2000 年 9 月 1 日改裝後以「玫瑰 99」開幕（店號 202）；玫瑰官網 2001 年 2 月與 4 月的門市表稱「音樂 99」，6 月已不在名單上。"),
    S("rose-ufo", "飛碟樂地 UFO 忠孝店（玫瑰）", "chain", "台北市大安區忠孝東路四段209號2樓", 1999, "e", 2003, "a", [146, 108, 106, 107, 109],
      "玫瑰併入飛碟集團後，1999 年 5 月 14 日開了第一家「飛碟樂地」（店號 101，第二家在中壢）。2001 年初官網稱「忠孝 UFO」，後改稱忠孝店，2002 年 6 月仍在名單上；淘兒 2003 年底退出後，忠孝店搬到頂好的忠孝東路四段 71-1 號。", "UFO"),
    S("rose-station", "玫瑰唱片 站前店（公園路）", "chain", "台北市中正區公園路22號之2", 1997, "e", 2006, "e", [146, 57, 106, 107, 109, 114, 139],
      "1997 年 7 月 30 日開幕。2000 年《秘密基地》提到玫瑰站前店「有高手坐鎮，是古典、爵士迷尋寶的地方」；玫瑰門市表從 2001 年一路列到 2006 年 10 月（2005 年寫明二樓到四樓），2007 年 1 月起不在名單上。"),
    S("rose-tongh0", "玫瑰唱片 通化店（文昌街）", "chain", "台北市大安區文昌街192號", 1998, "e", 2008, "e", [146, 106, 107, 109, 115],
      "1998 年 4 月 19 日開幕；玫瑰門市表 2001 年 2 月到 2008 年 1 月都列在文昌街，2008 年 4 月起改列通化街 26 之 4 號。"),
    S("rose-emei", "玫瑰唱片 峨嵋店", "chain", "台北市萬華區西寧南路62號2樓", 1999, "e", 2006, "e", [146, 106, 107, 109, 114, 139],
      "原為好樂迪體系的 ABCD 唱片，1999 年 12 月 4 日改以玫瑰峨嵋店開幕（店號 501）；玫瑰門市表 2001 年 2 月到 2006 年 1 月都列出，2006 年 7 月起不在名單上。隔壁 58 號 2004 年起是五大唱片。"),
    S("rose-tianmu", "玫瑰唱片 天母店", "chain", "台北市士林區天母西路13巷1號之1", 1996, "b", 2006, "e", [106, 107, 108, 109, 115, 117],
      "1996 年《音樂時代》名單已列出「天母玫瑰」在同一地址；公司沿革也說天母店是公館店之後最早開的分店之一。2006 年 1 月還在、5 月已無。"),
    S("rose-guangfu", "玫瑰唱片 光復店", "chain", "台北市大安區光復南路286號B1", 2001, "e", 2002, "u", [107],
      "2001 年 8 月的門市表還沒有，11 月起列出，2002 年 6 月仍在。"),
    S("rose-minsheng", "玫瑰唱片 民生店", "chain", "台北市松山區民生東路五段133號B1", 2001, "e", 2007, "e", [107, 109, 115],
      "2001 年 12 月起列出，一直到 2007 年 1 月；4 月起不在名單上。"),
    S("rose-tesco-sanmin", "玫瑰唱片 特易購三民店", "chain", "台北市松山區三民路160號", 2005, "b", 2006, "e", [109, 115],
      "開在英國特易購（Tesco）量販店內，2005 年 11 月與 2006 年 1 月的玫瑰門市表列出，7 月已無；特易購 2006 年退出台灣。"),
    S("rose-vieshow", "玫瑰唱片 威秀店", "chain", "台北市信義區松壽路20號", 2009, "e", 2011, "e", [109],
      "信義威秀影城 1 樓（1F-02）。2009 年 7 月的門市表還沒有，11 月起列出；2011 年 7 月還在、10 月已無。"),
    S("rose-breeze", "玫瑰唱片 微風店", "chain", "台北市松山區復興南路一段39號7樓", 2009, "e", 2011, "e", [109],
      "微風廣場 7 樓。2009 年 11 月起列出，2011 年 7 月還在、10 月已無。", geo="台北市大安區復興南路一段39號"),
    S("rose-qsquare", "玫瑰唱片 京站店", "chain", "台北市大同區市民大道一段209號5樓", 2010, "e", 2010, "a", [109],
      "京站時尚廣場 5 樓（2009 年底開幕）。2010 年 4 月與 7 月的門市表列出，2011 年 6 月已無。", geo="台北市大同區市民大道一段209號"),
    S("qianwei", "前衛唱片（大地之音 前衛店）", "chain", "台北市中正區開封街一段3號2樓", 2000, "b", 2003, "u", [57, 114],
      "2000 年《秘密基地》把「前衛」列為車站前的唱片行之一；2003 年 4 月前的店家清單寫作「大地之音唱片（前衛店）」，大地之音在基隆、鳳山、屏東也有分店。"),
    S("qianwei0", "前衛唱片（許昌街）", "chain", "台北市中正區許昌街8號1樓", 1996, "b", 1996, "u", [117],
      "1996 年《音樂時代》名單上的地址；之後搬到開封街，搬遷年不詳。"),
    S("abcd", "ABCD 唱片（好樂迪體系）", "chain", "台北市萬華區西寧南路62號2樓", 1999, "b", 1999, "e", [146, 57],
      "好樂迪 KTV 體系的唱片行（好樂迪西寧店也在西寧南路 62 號）。《秘密基地》稱它是西寧南路上的「後起之秀」，有「紅白標」促銷，店內設 DJ 台，店員會上台介紹新貨。依玫瑰的門市表，這家店 1999 年 12 月 4 日改為玫瑰唱片峨嵋店。開店年不詳。"),
    S("guanghua", "光華唱片 總店", "chain", "台北市中正區八德路二段25號2樓", 1996, "b", 2000, "u", [117, 57],
      "2000 年《秘密基地》說逛光華商場的樂迷，多半寧願到附近的「光華」和合友。地址取自 1996 年《音樂時代》名單（另列光華 A 店，八德路一段 51 號之 11 室）；2000 年時是否仍在同一地址、何時結束都不詳。",
      geo="台北市中山區八德路二段25號"),
    S("lingnav", "領航者唱片", "indie", "台北市萬華區西寧南路141號", 1996, "b", 2000, "u", [117, 57],
      "2000 年《秘密基地》稱它和佳佳都是西門町的老牌唱片行；地址取自 1996 年《音樂時代》名單，2000 年時是否仍在同一地址不詳。"),
    S("daidi-baoqing", "大地唱片 遠東百貨寶慶店專櫃", "chain", "台北市中正區寶慶路32號6樓", 1996, "b", 2003, "u", [114, 117],
      "遠東百貨寶慶店內的唱片專櫃；1996 年《音樂時代》名單列在 4 樓，2003 年 4 月前的店家清單列在 6 樓、寫作大地唱片。"),
    S("haishan-station", "海山唱片 新光三越站前店專櫃", "chain", "台北市中正區忠孝西路一段66號10樓", 2003, "b", 2003, "u", [114],
      "百貨公司內的唱片專櫃，只見於 2003 年 4 月前的店家清單。"),
    S("haishan-nyny", "海山唱片 紐約紐約專櫃", "chain", "台北市信義區松壽路12號3樓", 2003, "b", 2003, "u", [114],
      "紐約紐約購物廣場內的唱片專櫃，只見於 2003 年 4 月前的店家清單。"),
    S("fnac", "法雅客 FNAC 環亞店", "chain", "台北市松山區南京東路三段337號（環亞購物中心B1）", 1999, "e", 2009, "e", [53, 54, 57, 100],
      "1999 年 7 月開幕，1000 坪的多媒體賣場，初期有大型音樂區；2006 年法國 Fnac 撤資，音樂區縮小，環亞店 2009 年 10 月 12 日結束。地址依環亞購物中心。", "FNAC",
      geo="台北市松山區南京東路三段337號"),
    S("rose-tongh", "玫瑰唱片 通化店", "chain", "台北市大安區通化街26之4號2樓", 2008, "e", 2013, "e", [17, 109],
      "由文昌街搬遷至此，2008 年 4 月起出現在玫瑰門市表；2013 年 4 月還在、10 月已無，此後玫瑰在台北市沒有以玫瑰為名的門市。"),
    S("rose-chongqing", "玫瑰大眾 古典館（重慶南路）", "chain", "台北市中正區重慶南路一段15號1樓", 2022, "e", 2026, "e", [105, 15, 16, 63, 10],
      "全台最後一家玫瑰大眾實體店，2026 年 11 月 30 日結束營業。"),
    S("rose-xuchang30", "玫瑰唱片 許昌店", "chain", "台北市中正區許昌街30號B1", 2001, "e", 2004, "a", [106, 107, 109, 114],
      "玫瑰官網 2001 年 6 月的門市表還沒有，8 月起列出（B1–B2 兩層），與公園路的站前店同時營業；2005 年 11 月的門市表已無，結束時間在 2002–2005 年之間。"),
    S("rose-ximen0", "玫瑰唱片 西門店（萬國百貨旁）", "chain", "台北市萬華區峨嵋街37-43號2樓", 1997, "e", 2003, "u", [146, 57, 106, 107, 114, 139],
      "1997 年 3 月 14 日開幕。2000 年《秘密基地》形容它「有陣勢驚人的試聽機，沿著窗邊一家排開」；玫瑰官網 2001–2002 年都列出，2003 年 4 月前的店家清單仍有，2005 年的門市表已無；那時西門町的玫瑰是漢中街的加州玫瑰。", geo="台北市萬華區峨眉街37號"),
    S("rose-ximen", "加州玫瑰 西門店", "chain", "台北市萬華區漢中街52號", 2005, "b", 2011, "e", [15, 109, 115],
      "玫瑰門市表 2005 年 11 月已列出「加州」（漢中街 52 號 1 樓），2011 年改到地下樓，7 月還在、10 月已無。維基百科記載 2009 年 8 月 1 日重新開幕，可能是改裝。"),
    S("cosmos", "宇宙城唱片 公館店", "chain", "台北市中正區汀州路三段194號2樓之1", 1989, "e", 2000, "e", [146, 57, 62, 16, 108, 117],
      "從西門町起家的唱片行，被玫瑰購併。玫瑰的門市表記載公館宇宙城 1989 年 5 月 13 日開幕、2000 年 9 月 1 日改裝重新開幕，同一天這裡以「玫瑰 99」開張。1996 年《音樂時代》名單列在汀州路三段 194 號 2 樓之 1，2000 年《秘密基地》說它在公館金石堂廣場二樓。"),
    S("tachung-ntu", "大眾唱片 台大店", "chain", "台北市大安區新生南路三段104號2-4樓", 2000, "b", 2012, "e", [57, 91, 58, 110, 114, 139],
      "三層樓的大眾唱片。G-Music 大眾門市表列到 2012 年 10 月，2013 年 1 月起不在名單上；2012 年 3 月就傳出即將結束。"),
    S("tachung-xuchang", "大眾唱片 許昌店（後為玫瑰大眾古典館）", "chain", "台北市中正區許昌街24號", 2000, "b", 2021, "e", [57, 91, 60, 58, 66, 110, 15, 114, 139],
      "大眾官網 2001–2005 年列為站前一店（許昌街 20-24 號），之後稱許昌店（2010 年起寫作 24-2 號 2 樓），一直列到 2014 年。2016 年的玫瑰大眾購物網稱它「大眾唱片許昌古典館」，也就是後來的玫瑰大眾古典館（24-1 號 2 樓），2016 年起是全台唯一的玫瑰大眾門市，2022 年遷往重慶南路。", geo="台北市中正區許昌街24號"),
    S("tachung-st2", "大眾唱片 站前二店", "chain", "台北市中正區許昌街28號", 2001, "b", 2001, "a", [91],
      "2001 年 6 月的大眾官網列出，同年 12 月已不在名單上。"),
    S("tachung-st2b", "大眾唱片 站前二店（再次列出）", "chain", "台北市中正區許昌街28號", 2004, "b", 2004, "u", [91],
      "2001 年底從大眾官網消失後，2004 年 12 月的門市表又列出站前二店，之後的狀況不詳。", geo="台北市中正區許昌街28號"),
    S("tachung-gg", "大眾唱片 公館店", "chain", "台北市文山區羅斯福路四段114號", 2000, "b", 2005, "a", [57, 91, 58, 110, 139],
      "2000 年《秘密基地》與 2001–2004 年大眾官網都有列；2005 年 10 月的大眾門市表在台北市只剩台大與許昌，公館店應在這之前結束。這個地址後來是光南大批發公館店。",
      geo="台北市中正區羅斯福路四段114號"),
    S("tachung-sl", "大眾唱片 士林店", "chain", "台北市士林區大東路11-6號", 2001, "b", 2005, "a", [91, 110, 139],
      "士林夜市旁，營業到凌晨一點；2004 年 12 月的大眾官網仍列出，2005 年 10 月已不在名單上。"),
    S("tachung-xm", "大眾唱片 西門店", "chain", "台北市萬華區漢中街116號2樓", 2002, "a", 2003, "a", [91],
      "2002 年 10 月與 2003 年初的大眾官網列出，2004 年已不在名單上。"),
    S("rose-dinghao", "玫瑰唱片 忠孝店（頂好）", "chain", "台北市大安區忠孝東路四段71-1號2樓", 2004, "a", 2009, "e", [11, 109, 115],
      "淘兒 2003 年底退出後，玫瑰的忠孝店從忠孝東路四段 209 號搬到頂好這個地址，2005 年 11 月的門市表已在此；2009 年 1 月還在、4 月已無，之後由五大接手。"),
    S("5music-dinghao", "五大唱片 忠孝店（頂好）", "chain", "台北市大安區忠孝東路四段71-1號2樓", 2009, "e", 2020, "e", [11, 17, 66, 90],
      "與當年東淘、後來的玫瑰同一地址；五大在 2009–2020 年經營這家門市。"),
    S("5music-ximen1", "五大唱片 西門店（西寧南路）", "chain", "台北市萬華區西寧南路58號", 2004, "e", 2016, "a", [59, 17, 13, 66],
      "2004 年 7 月起租下這棟五層樓；租約訴訟後約 2015 年底被判遷出。"),
    S("5music-ximen2", "五大唱片 西門店（武昌街）", "chain", "台北市萬華區武昌街二段18號2樓", 2016, "a", 2021, "a", [13, 11, 90],
      "遷入年依西寧南路店遷出推估；2019 年已在此，2022 年 1 月店面已在招租。"),
    S("5music-xuchang", "五大唱片 許昌店（站前）", "chain", "台北市中正區許昌街34、36號2樓", 2009, "e", 2024, "a", [86, 66, 67, 13, 90],
      "2009 年 2 月登記的許昌分公司，2014 年名單稱許昌店；2019 年從兩層縮成一層。2024 年搬到對面南陽街 1 號 2 樓。"),
    S("5music-station", "五大唱片 台北站前店（許昌店）", "chain", "台北市中正區南陽街1號2樓", 2024, "e", None, None, [18, 5, 87],
      "2024 年 5 月搬到原址對面的二樓，站前新光三越旁；官網仍以 Xuchang 稱之。目前台北唯一一家五大。"),
    S("chiachia-zhonghua", "佳佳唱片 中華店（西門總店）", "chain", "台北市萬華區中華路一段110號2、3樓", 1992, "e", None, None, [0, 6, 11, 13, 66, 90, 57, 117, 139],
      "1976 年開在中華商場，1992 年商場拆除後搬到西門町現址。", "Chia Chia Records"),
    S("chiachia-hankou0", "佳佳唱片 漢口店（一樓）", "chain", "台北市中正區漢口街一段3號", 1998, "e", 2015, "e", [112, 111, 113, 139],
      "1998 年開設，2001 年 PTT 商店情報已列出漢口街一段 3 號；2015 年 4 月 1 日搬到同址的地下樓。", "Chia Chia Records"),
    S("chiachia-hankou", "佳佳唱片 漢口店", "chain", "台北市中正區漢口街一段3號B1", 2015, "e", None, None, [17, 0, 5, 11, 13, 66, 90, 113],
      "2015 年 4 月 1 日從一樓搬到同址的地下樓，入口在隔壁樓梯。", "Chia Chia Records"),
    S("chiachia-zx", "佳佳唱片 忠孝店", "chain", "台北市中正區忠孝西路一段49號B1", 2013, "b", 2014, "e", [17, 61],
      "台北車站地下街誠品捷運商場內；2014 年 6 月改名樂樂唱片。"),
    S("lele", "樂樂唱片", "indie", "台北市中正區忠孝西路一段49號B1", 2014, "e", 2015, "a", [61, 83, 66],
      "佳佳忠孝店 2014 年 6 月改名而來，2015 年 7 月清倉特賣，之後應已歇業。2014 年名單寫作 50 號 2 樓，可能與佳佳站前店混淆。"),
    S("chiachia-station", "佳佳唱片 台北站前店", "chain", "台北市中正區忠孝西路一段50之1號B1", 2013, "b", 2014, "a", [17, 123],
      "原本開在新光三越前的站前地下街，後來搬到五鐵秋葉原樓上，不久就結束；搬遷年份與新店樓層不詳，地圖只標地下街的位置。"),
    S("eslite-ntu", "誠品音樂館 台大店", "chain", "台北市大安區新生南路三段98號（誠品台大店後方巷內）", 1999, "e", 2002, "a", [57, 36],
      "誠品第一家音樂館，1999 年底開幕，約 2002 年移到敦南。地址以誠品台大店標示。", "Eslite", geo="台北市大安區新生南路三段98號"),
    S("eslite-dunnan", "誠品音樂館 敦南店", "chain", "台北市大安區敦化南路一段245號B2", 2002, "a", 2020, "e", [17, 24, 36, 66, 90],
      "約 2002 年由台大移來；敦南店 2020 年 5 月 31 日歇業。", "Eslite"),
    S("eslite-xinyi", "誠品音樂館 信義店", "chain", "台北市信義區松高路11號4樓", 2006, "e", 2023, "e", [17, 4, 37, 66, 90],
      "誠品信義店 2006 年 1 月 1 日開幕，2023 年 12 月 24 日歇業。", "Eslite"),
    S("eslite-songyan", "誠品音樂 松菸黑膠館", "chain", "台北市信義區菸廠路88號3樓", 2014, "b", None, None, [66, 3, 11, 37, 90],
      "2014 年名單已列出松菸黑膠館；誠品信義店歇業後，2024 年 1 月這裡改為 24 小時音樂館，賣黑膠、CD 與唱盤。", "Eslite"),
    S("knn-xuchang0", "光南大批發 許昌店（40號）", "chain", "台北市中正區許昌街40號", 2000, "b", 2024, "e", [57, 103, 13, 90, 11, 114, 139],
      "2000 年《秘密基地》已列出車站前的光南；2003 年前的店家清單在許昌街 40 號 1 樓列出「光進唱片」，電話與地址看來是光南的誤植。2009 年門市清單在許昌街 40 號，是當時台北市唯一的光南。一樓有 CD／DVD 區，2024 年 10 月搬到隔壁 36 號。"),
    S("knn-gongguan", "光南大批發 公館店", "chain", "台北市文山區羅斯福路四段114號", 2014, "b", None, None, [104],
      "與當年大眾唱片公館店同一個地址；2014 年的門市清單已列出。", geo="台北市中正區羅斯福路四段114號"),
    S("knn-xuchang", "光南大批發 許昌店（36號）", "chain", "台北市中正區許昌街36號", 2024, "e", None, None, [11]),
    S("syntrend-vinyl", "三創黑膠", "chain", "台北市中正區市民大道三段2號5樓", 2015, "e", 2026, "e", [138, 12, 7, 90, 123],
      "三創生活園區自有品牌的黑膠店，2015 年 5 月隨園區開幕，號稱全台庫藏最多；2026 年歇業。", geo="台北市中正區市民大道三段2號"),

    # ---- 獨立唱片行（新品／二手 CD 為主） ----
    S("shangyang", "上揚唱片", "indie", "台北市中山區中山北路二段77-4號", 1967, "e", None, None, [2, 7, 66, 90, 117],
      "1967 年創立，以古典音樂與本土歌謠聞名，兼營唱片發行。1996 年《音樂時代》名單登記在中山北路二段 77 巷 9 號 4 樓。"),
    S("95", "九五樂府", "indie", "台北市萬華區漢口街二段20巷11號", 1976, "e", None, None, [19, 13, 7, 66, 90, 57, 117],
      "以日本進口唱片為主的老店，原本是漢口街巷弄裡的小店，也是重金屬迷代訂進口 CD 的去處。約 1997 年另開較大的分店，見「九五樂府（武昌街）」。"),
    S("95-wuchang", "九五樂府（武昌街）", "indie", "台北市萬華區武昌街二段47號", 1996, "b", 2000, "u", [117, 57],
      "2000 年《秘密基地》寫九五約 1997 年在西寧南路附近開了一家面積較大的分店，滿是日本 CD 與周邊，也保留一面重金屬架。1996 年《音樂時代》名單上九五登記在武昌街二段 47 號，就在西寧南路旁，推測是同一家店；歇業年不詳。"),
    S("rk", "駱克唱片行（南京東路）", "indie", "台北市松山區南京東路五段123巷1弄19號", 2007, "e", 2021, "e", [120, 119, 20, 17, 66, 90],
      "2007 年 7 月由東區搬遷至此（PTT 古典音樂板 2007 年 5 月的貼文預告）；2021 年 2 月 9 日在此營業到最後一天，3 月 2 日搬到光復北路。", "RK Record"),
    S("rk0", "駱克唱片行（東區）", "indie", "台北市大安區忠孝東路四段216巷11弄18號", 1994, "e", 2007, "e", [118, 117, 120, 20],
      "1994 年 7 月開在明曜百貨後面的巷子裡，店名從巴洛克、洛克演變成駱克；老闆原本想開的是音樂圖書館。開店三年後開始賣二手卡帶與 CD。1996 年《音樂時代》名單列在這個地址，2007 年 7 月搬到南京東路五段。", "RK Record"),
    S("rk2", "駱克唱片行（光復北路）", "indie", "台北市松山區光復北路85巷21號1樓", 2021, "e", None, None, [119, 20, 7],
      "2021 年 3 月 2 日在新址開幕。", "RK Record", geo="台北市松山區光復北路85巷21號"),
    S("indimusic", "個體戶唱片行", "indie", "台北市大安區羅斯福路三段297-5號3樓", 2001, "a", None, None, [6, 17, 23, 19, 66, 90, 57],
      "二手黑膠與 CD，偏重金屬與硬式搖滾。約 1996 年起家，前幾年在新生南路，約 2001 年起在現址；各報導年資說法不一。", "Indimusic Records"),
    S("hoyou", "合友唱片", "indie", "台北市中正區八德路一段82巷12號", 2000, "b", None, None, [12, 11, 7, 66, 90, 57, 117],
      "光華商圈的老唱片店，公司 1994 年登記。1996 年《音樂時代》名單上合友在民生東路五段，這個地址當時列的是「學友 B」；2000 年《秘密基地》已把合友列在光華商圈。CD、DVD 與不少黑膠。"),
    S("hoyou0", "合友唱片（民生東路）", "indie", "台北市松山區民生東路五段72號", 1996, "b", 1996, "u", [117],
      "1996 年《音樂時代》名單上的地址；2000 年已在光華商圈。"),
    S("aile1", "愛樂唱片（漢口街）", "indie", "台北市中正區漢口街一段10號3樓", 2013, "b", 2020, "u", [17, 13, 66, 90], "二手唱片，CD 庫存多。"),
    S("aile2", "愛樂唱片（重慶南路）", "indie", "台北市中正區重慶南路一段44號3樓", 2026, "b", None, None, [7]),
    S("qiyuan1", "啟元唱片（重慶南路）", "indie", "台北市中正區重慶南路一段49號B1", 2000, "b", 2004, "u", [17, 57, 94], "二手 CD 兼黑膠與音響器材；2004 年仍在重慶南路，2014 年名單已在林森北路。"),
    S("qiyuan2", "啟元唱片（林森北路）", "indie", "台北市中正區林森北路5巷8號", 2014, "b", None, None, [142, 17, 12, 66, 90],
      "善導寺站附近；二手 CD、DVD 與黑膠，2026 年仍營業。"),
    S("zelong0", "澤龍音樂（成都路22號）", "indie", "台北市萬華區成都路22號1樓", 1994, "a", 2019, "a", [73, 66, 67, 13, 114],
      "1994 年 12 月登記的唱片公司，西門捷運 6 號出口旁；2003 年前的店家清單寫作成都路 24 號 1、2 樓。搬遷年不詳，推估約 2019–2020 年。"),
    S("zelong", "澤龍唱片（紅樓旁）", "indie", "台北市萬華區成都路10巷15號", 2020, "a", None, None, [74, 7, 90], "紅樓廣場旁，CD、DVD、藍光，流行、古典與戲曲都有。"),
    S("yuanyuan", "元元唱片（士林夜市）", "indie", "台北市士林區大東路10-5號", 2003, "b", 2003, "u", [114, 116, 139],
      "2003 年 4 月前的店家清單列出士林夜市的大東路 10-5 號；PTT 士林板有網友記得元元在光華戲院一帶與士林夜市都有店面；2003 年 3 月的歌手答謝唱片行行程，在士林還列了元元的文林、基河、士林中正三家分店（門牌不詳，未標上地圖）。開業與結束年份不詳。"),
    S("jiesheng", "傑笙唱片（原名小林）", "indie", "台北市中山區中山北路三段17號2樓", 2000, "b", 2013, "u", [17, 66, 57, 117],
      "直接從英、德、義、美、日、荷進口台灣未代理的廠牌，以重搖滾、前衛搖滾與死亡、黑金屬聞名；2014 年起的名單標為已歇業。"),
    S("jiesheng0", "傑笙唱片（農安街）", "indie", "台北市中山區農安街22號", 1996, "b", 1996, "u", [117],
      "1996 年《音樂時代》名單上的地址；2000 年已在中山北路三段。"),
    S("xiaocai-zh", "小蔡的店 臺北店", "indie", "台北市萬華區中華路二段426號之5", 2000, "b", 2013, "u", [17, 57], "二手 CD。"),
    S("xiaocai-xm", "小蔡的店 西門店", "indie", "台北市萬華區峨嵋街55號2樓", 2013, "b", 2014, "u", [17, 66], "二手 CD。", geo="台北市萬華區峨眉街55號"),
    S("xiaocai-sl", "小蔡的店 士林店", "indie", "台北市士林區大南路12號2樓", 2013, "b", 2013, "u", [17], "二手 CD。"),
    S("mollie", "茉莉二手書店 影音館（台大）", "indie", "台北市大安區羅斯福路四段24巷13號B1", 2013, "b", 2019, "u", [17, 14, 7, 66, 90], "二手 CD、卡帶與黑膠。"),
    S("regen-gg", "再生工場 公館店", "indie", "台北市中正區羅斯福路三段312號B1", 2000, "b", 2020, "u", [17, 14, 90, 57], "二手 CD、特價 CD 與影碟；2000 年《秘密基地》已列為公館唱片行之一。"),
    S("mondian", "蒙得你安二手唱片", "indie", "台北市大安區忠孝東路四段248巷13號", 2000, "b", 2013, "u", [17, 57]),
    S("mondian2", "蒙得你安唱片 Mondrian Vinyls", "indie", "台北市松山區八德路三段74巷（門牌不詳）", 2026, "b", None, None, [125],
      "Google 地圖上營業中的黑膠店，標示「個人深度黑膠聆聽體驗」，位在 Soil 咖啡樓下。店名與 2000 年代東區的蒙得你安二手唱片相同，是否為同一家、何時開業都不詳，因此分開列出；位置依 Google 地圖標示。",
      geo="台北市松山區八德路三段74巷94號"),
    S("btb", "沒有新歌的唱片行", "indie", "台北市大安區和平東路一段12巷4號", 2014, "e", 2024, "e", [32, 20, 19, 66, 90],
      "以 2000 年前的音樂為主，CD、黑膠與卡帶；2024 年 4 月 30 日結束實體店。", "BTB Music Workshop"),
    S("species", "有種唱片 Species Records", "indie", "台北市萬華區昆明街96巷20號2樓", 2004, "a", 2020, "u", [17, 8, 66, 90],
      "電子、House、Techno 新舊黑膠，可試聽與練 DJ。約 2004 年開店；2017 年後是否營業各方說法不一。", "Species Records"),
    S("metalgate", "搖滾帝國／金屬極境 Metal Gate", "indie", "台北市松山區八德路四段389巷38號", 2020, "b", None, None, [7, 90], "金屬樂。"),
    S("pubmetal", "陰府門 Pub Metal", "indie", "台北市萬華區昆明街136巷1弄10號B1", 2020, "b", None, None, [7, 90], "金屬樂周邊與唱片。"),

    # ---- 黑膠與複合店 ----
    S("wabbit-wall", "小白兔唱片（The Wall）", "indie", "台北市文山區羅斯福路四段200號B1", 2003, "a", 2012, "e", [27, 28],
      "1999 年在光華商場的「聖界」起家，約 2003 年起設在 The Wall 展演空間內，2012 年 1 月結束。", "White Wabbit Records"),
    S("wabbit", "小白兔唱片（師大）", "indie", "台北市大安區浦城街21巷1-1號", 2009, "e", None, None, [27, 0, 4, 7, 19, 23, 66, 90],
      "2009 年 7 月開的師大店，現在是小白兔唯一的門市，兼營獨立音樂廠牌與代理。", "White Wabbit Records"),
    S("mam", "M@M Records 四樓唱片行", "indie", "台北市大安區忠孝東路四段112號4樓之3", 1999, "e", 2016, "a", [31, 0, 66, 57],
      "1999 年開業，辦公大樓四樓的電子樂黑膠店；曾停業兩年多。"),
    S("mam2", "M@M Records（重新開幕）", "indie", "台北市大安區忠孝東路四段112號4樓之3", 2019, "e", None, None, [31, 0, 90],
      "停業兩年多後 2019 年在原址重新開幕，賣電子、搖滾與 Hip Hop 黑膠。"),
    S("tht1", "THT 黑膠唱片行（興安街）", "combo", "台北市中山區興安街10-2號", 2018, "a", 2024, "e", [4, 6, 22, 40, 90],
      "黑膠唱片行兼咖啡與酒吧；2024 年 6 月搬到松山。", "THT Records"),
    S("tht-room25", "THT 二店 Room 25", "indie", "台北市中山區興安街6-1號", 2023, "e", 2024, "u", [22], "", "THT Records"),
    S("tht2", "THT 黑膠音樂圖書館", "combo", "台北市松山區復興北路427巷16號1樓", 2024, "e", None, None, [22], "2024 年 6 月底開幕。", "THT Records"),
    S("waiting0", "Waiting Room（泰順街）", "indie", "台北市大安區泰順街（門牌不詳）", 2011, "a", 2015, "e", [29],
      "第一家店開在泰順街公寓二樓，門牌不詳，地圖上標在泰順街中段。", geo="台北市大安區泰順街40號"),
    S("waiting", "Waiting Room（中山）", "indie", "台北市中山區長安西路40巷10弄1號", 2015, "e", None, None, [29, 4, 7], "2015 年搬到中山。新品黑膠、獨立音樂與爵士，兼賣服飾與藝術書。"),
    S("agoodday", "風和日麗唱片行", "indie", "台北市大安區和平東路三段212巷18號1樓", 2015, "e", 2019, "e", [30, 6, 23],
      "風和日麗唱片的直營店，2019 年 12 月 1 日歇業。", "A Good Day Records"),
    S("vinyldecision1", "Vinyl Decision 黑膠咖啡（崇德街）", "combo", "台北市信義區崇德街38巷6號", 2014, "e", 2022, "a", [49, 38, 4, 23, 90],
      "2014 年 3 月在六張犁附近開店的黑膠咖啡，後來搬到華山。"),
    S("vinyldecision2", "Vinyl Decision（華山）", "combo", "台北市中正區八德路一段1號（華山1914 紅磚區西7-4館）", 2022, "a", None, None, [38, 19, 7],
      "2021 年底在華山快閃，之後進駐紅磚區。", geo="台北市中正區八德路一段1號"),
    S("2manyminds0", "貳樂號 2manyminds Records（瑞安街）", "indie", "台北市大安區瑞安街136號2樓", 2014, "e", 2015, "a", [77, 78, 66],
      "DJ Spykee 開的初代店，日本音樂、電影、雜誌與樂團 T 恤。2014 年 11 月仍在瑞安街。"),
    S("2manyminds", "貳樂號 2manyminds Records（羅斯福路）", "indie", "台北市文山區羅斯福路四段206巷8號", 2015, "a", 2018, "a", [33, 78, 4],
      "The Wall 後方；2016 年 9 月已在此。店主 2018 年底轉任 The Wall 總監，之後歇業。"),
    S("beansbeats", "BEANS & BEATS", "indie", "台北市松山區富錦街346號1樓", 2014, "e", 2021, "u", [34, 4, 66, 90], "2014 年 10 月開幕，美式街頭音樂黑膠。"),
    S("xiaosong1", "小宋唱片（西園路二段79號）", "indie", "台北市萬華區西園路二段79號", 1994, "a", 2018, "a", [39, 4, 66],
      "二手黑膠，爵士、古典與華語台語老歌。開業年有 1994 與 1997 兩種說法；2014 年還在 79 號，2020 年已在 225 巷，搬遷年不詳。"),
    S("xiaosong", "小宋唱片（西園路二段225巷）", "indie", "台北市萬華區西園路二段225巷10號", 2019, "a", None, None, [145, 6, 39, 0, 90],
      "二手黑膠，古典、爵士與華語、日本老歌；2026 年仍營業。"),
    S("analogy", "古殿樂藏", "combo", "台北市北投區西安街一段169號2樓", 2020, "b", None, None, [6, 7, 90], "古典黑膠與音樂沙龍，需預約。", "Classical Palace Society"),
    S("blackglue", "Black Glue Records", "indie", "台北市大安區復興南路二段332號", 2026, "b", None, None, [7]),
    S("soulamazin", "Soul Amazin' Music", "indie", "台北市信義區永吉路523號2樓", 2020, "b", None, None, [7, 90]),
    S("datao", "大韜黑膠耳機專賣 北流店", "indie", "台北市南港區忠孝東路七段99號1樓", 2022, "e", None, None, [1, 5],
      "2022 年 9 月開幕，庫存約三萬多張二手黑膠，號稱全台最大的黑膠店。", "DaTao Vinyl"),
    S("slipped", "摔碟唱片舍 Slipped Disk", "combo", "台北市大安區瑞安街276巷14號1樓", 2025, "e", None, None, [21, 35],
      "2025 年 8 月 6 日開幕的二手黑膠店，附試聽區與精釀啤酒吧台。"),
    S("avc", "AVC Coffee Roasters", "combo", "台北市中山區新生北路二段53-3號", 2026, "e", None, None, [26],
      "2026 年開幕的黑膠咖啡廳，販售黑膠與 CD。"),
    # ---- 第二輪補充 ----
    S("diyi", "第一唱片行", "indie", "台北市大同區保安街88號", 1965, "e", None, None, [52, 90, 123],
      "大稻埕的台語歌謠唱片老店，早年也是唱片公司，現由第三代經營，2026 年仍在營業。"),
    S("xintianxindi", "新天新地（錦西街）", "indie", "台北市大同區錦西街1-1號3樓", 2004, "e", 2013, "a", [50, 88],
      "前淘兒員工林主惟創辦，專賣歐陸、以法國為主的獨立廠牌 CD，後來兼營音響。更早曾在忠孝東路、善導寺一帶，年份不詳。"),
    S("xintianxindi2", "新天新地 2（復興南路）", "indie", "台北市大安區復興南路二段185-1號", 2014, "e", 2019, "e", [88, 66, 89],
      "2014 年 3 月 4 日開幕，2019 年 10 月 12 日結束。"),
    S("xintianxindi3", "新天新地 3（安和路）", "indie", "台北市大安區安和路二段184巷3號2樓", 2019, "e", None, None, [88, 89, 90],
      "2019 年 12 月 6 日開幕，週四到週六營業。"),
    S("juexiang", "絕響", "indie", "台北市士林區基河路350號", 2008, "b", 2008, "u", [50], "發燒古典、爵士與人聲 CD，以網路販售為主。"),
    S("impo0", "IMPO 唱片（羅斯福路三段254號）", "indie", "台北市中正區羅斯福路三段254號2樓", 2002, "b", 2008, "a", [96, 97],
      "前淘兒台灣區經理楊傑格開設，以進口獨立搖滾為主，早期有四、五家分店；2000 年已創辦音樂刊物 T-MAG。"),
    S("impo", "IMPO 唱片（316巷）", "indie", "台北市中正區羅斯福路三段316巷16號3樓", 2009, "b", None, None, [140, 49, 66, 90, 97], "公館捷運站 4 號出口附近的三樓小店，2009 年起在此，兼賣二手 CD、黑膠與進口代訂；2026 年仍營業，週六、日下午開門。"),
    S("laobanniang", "老闆娘的店", "indie", "台北市中山區民權東路一段53號", 1994, "e", 2016, "e", [122, 117],
      "1994 年開店、2016 年結束；1996 年《音樂時代》名單也列出這個地址。"),
    S("38c", "攝氏三十八度音響唱片", "indie", "台北市中正區重慶南路二段90之1號", 2000, "b", None, None, [49, 41, 66, 90, 57, 123],
      "音響器材兼賣唱片。攝氏三十八度音響唱片有限公司 1989 年設立；當時是否就在這個地址不詳，地圖從最早有紀錄的 2000 年畫起。"),
    S("longfeng", "龍鳳唱片", "indie", "台北市萬華區華西街46號（華西街觀光夜市 8、10 號攤）", 2020, "b", None, None, [41, 90], "夜市裡的唱片攤，位置標在華西街上。",
      geo="台北市萬華區華西街46號"),
    S("senko1", "先行一車（師大路）", "indie", "台北市大安區師大路102巷8號", 2014, "e", 2022, "a", [44, 45, 66, 90],
      "二手黑膠與實驗音樂，也是唱片廠牌。", "Senko Issha Records"),
    S("senko2", "先行一車（泰順街）", "indie", "台北市大安區泰順街12號", 2022, "a", None, None, [41, 45], "約 2022 年搬到泰順街。", "Senko Issha Records"),
    S("sidoli", "小島裡 Sidoli Radio", "indie", "台北市大同區長安西路245號", 2020, "e", None, None, [47, 43], "舊防空洞改成的店，卡帶為主，也有黑膠。"),
    S("soundsgood", "聲色 Sounds Good", "combo", "台北市大安區新生南路二段30巷1-3號", 2021, "e", None, None, [46, 47],
      "2021 年 11 月開的黑膠與卡帶咖啡，店內可刻錄黑膠。"),
    S("dalangman", "大浪漫商店 台北", "indie", "台北市大安區潮州街102號（台北月見ル君想フ內）", 2022, "b", 2023, "u", [51, 43],
      "東京廠牌商店的台北據點，賣黑膠、卡帶與 T 恤。地址來自第三方店家資訊。", geo="台北市大安區潮州街102號"),
    S("chaobar", "潮電 ChaoBar & RecordStore", "combo", "台北市大安區潮州街76號2樓", 2024, "e", None, None, [48, 42],
      "2024 年 11 月試營運，舊台電建築裡的電子音樂聆聽酒吧兼唱片行。"),
    S("rotten", "爛調唱片 Rotten Blues", "indie", "台北市中正區汀州路二段197號", 2024, "b", None, None, [42, 41], "日版黑膠與 CD、二手黑膠。"),
    S("candle0", "燭光唱片（新生南路）", "indie", "台北市中正區新生南路一段108號3樓", 2023, "e", 2024, "e", [141],
      "2023 年 3 月開幕；2024 年 4 月因都市更新搬遷。"),
    S("candle1", "燭光唱片（信義路）", "indie", "台北市中正區信義路二段45巷19號1樓", 2024, "e", 2026, "e", [141, 42],
      "東門市場旁，2024 年 5 月起在此；2026 年 4 月又因都市更新搬遷。"),
    S("candle", "燭光唱片", "indie", "台北市中正區汀州路二段219號1樓", 2026, "e", None, None, [141, 41],
      "黑膠兼音響，主辦放碟祭；2026 年 5 月搬到汀州路。"),
    S("parstore", "PAR Store", "indie", "台北市大同區赤峰街3巷1號B1", 2020, "b", None, None, [41, 90], "選品店，有黑膠、卡帶與 zine。"),
    # ---- 韓國流行專輯店 ----
    S("kmonstar-zs", "K-MONSTAR 中山門市", "kpop", "台北市大同區赤峰街49巷7號1樓", 2023, "e", None, None, [65, 132, 64, 41],
      "K-MONSTAR 2023 年在赤峰街開出台灣第一家實體店。"),
    S("kmonstar-ns", "K-MONSTAR 微風南山門市", "kpop", "台北市信義區松智路17號B1", 2024, "e", None, None, [65, 132, 64, 41], "2024 年 5 月開幕。",
      geo="台北市信義區松智路17號"),
    S("kmonstar-bf", "K-MONSTAR 微風廣場門市", "kpop", "台北市松山區復興南路一段39號GF", 2025, "e", None, None, [133, 132, 41], "2025 年 4 月底開幕。", geo="台北市松山區復興南路一段39號"),
    S("willmusic1", "微樂客 Will Music 赤峰門市", "kpop", "台北市大同區赤峰街12巷5號1樓", 2024, "e", None, None, [121, 64, 41],
      "2017 年起在網路販售進口音樂商品，2024 年 3 月在赤峰街開出第一家實體門市試營運，也有黑膠區。"),
    S("willmusic2", "微樂客 Will Music 南西旗艦店", "kpop", "台北市中山區中山北路二段16巷25號2樓", 2026, "e", None, None, [129, 130, 41],
      "2026 年 1 月辦理門市登記，5 月的報導已列入。"),
    S("willmusic-att", "微樂客 Will Music ATT 4 FUN", "kpop", "台北市信義區松壽路12號5樓", 2025, "b", None, None, [131, 130],
      "2024 年 10 月辦理門市登記，2025 年 10 月的店家整理已列入，開幕月份不詳。"),
    S("willmusic-one", "微樂客 OneMusic 赤峰", "kpop", "台北市大同區赤峰街71巷26號1樓", 2025, "e", None, None, [131, 130],
      "2025 年 4 月辦理門市登記，同年 10 月的店家整理已列入。"),
    S("willmusic-ximen", "微樂客 Will Music 西門", "kpop", "台北市萬華區西寧南路50巷13-1號2樓", 2025, "e", None, None, [131, 130],
      "報導預告 2025 年 10 月 31 日起試營運。"),
    S("platbum", "PLATBUM", "kpop", "台北市中山區南京西路23巷1-3號2樓", 2026, "b", None, None, [129],
      "以男團專輯與周邊為主，店名取 platform 與 album 合成。"),
    S("fairytree1", "仙女樹 fairytree（敦化南路）", "kpop", "台北市大安區敦化南路一段177巷25號之2", 2024, "e", 2025, "u", [126, 128, 64],
      "2024 年開出第一家實體店，2025 年 10 月的報導仍列這個地址。之後搬到中山北路，確切月份不詳。"),
    S("fairytree2", "仙女樹 fairytree（中山北路）", "kpop", "台北市中山區中山北路二段36巷27號", 2026, "b", None, None, [129, 127, 41],
      "從東區搬到中山北路二段，二樓有拆專區。"),
    S("ygm", "YGM STORE", "kpop", "台北市大安區敦化南路一段177巷14號", 2024, "b", 2024, "u", [64]),
    S("hanju", "韓居 HG music 赤峰一店", "kpop", "台北市大同區赤峰街47巷16號1樓", 2025, "e", None, None, [133, 134, 41],
      "原本在官網與蝦皮販售，2025 年 5 月底開出實體店。"),
    S("hanju2", "韓居 HG music 赤峰二店", "kpop", "台北市大同區赤峰街47巷15號1樓", 2026, "b", None, None, [129, 134],
      "與一店隔著巷子相對，一間賣男團、一間賣女團。"),
    S("koreepop", "KOREEPOP 西門", "kpop", "台北市萬華區成都路32號1樓", 2025, "e", None, None, [137, 41], "官網寫自 2025 年 9 月 8 日起營運。"),
    S("allmyday1", "ALL MY DAY 中山（赤峰街）", "kpop", "台北市大同區赤峰街23巷15號", 2025, "e", None, None, [135, 136, 41],
      "經營公司自述 2025 年開出中山門市。"),
    S("allmyday2", "ALL MY DAY 信義", "kpop", "台北市信義區莊敬路423巷8弄10號", 2024, "e", None, None, [135, 41],
      "2017 年起經營網路賣場，2024 年底在信義開出第一家實體店。"),
    # ---- 2014 年名單補充 ----
    S("xiaomin", "小閔的古典音樂世界", "indie", "台北市中正區中山南路21-1號（國家音樂廳）", 2005, "e", 2014, "e", [68, 69, 66],
      "國家音樂廳一樓的古典 CD／DVD 專賣店，2005 年 3 月開幕，2014 年底結束，之後改在網路與音樂會現場販售。", geo="台北市中正區中山南路21-1號"),
    S("cheery", "巨禮音響唱片", "indie", "台北市士林區中山北路六段188號", 1986, "e", None, None, [70, 66],
      "1986 年起經營的音響代理商，兼賣歐美發燒唱片。", "Cheery Music"),
    S("joyaudio", "JOY AUDIO 發燒專門店", "indie", "台北市中正區中華路二段75巷6號", 2000, "a", None, None, [71, 66, 67, 90],
      "發燒片專門店，LP、CD、SACD、XRCD 與二手 CD；公司 2000 年登記。"),
    S("windsong", "韻順唱片", "indie", "台北市大同區民生西路45巷3弄1號", 1990, "a", None, None, [72, 67, 66, 90],
      "1989 年創立的古典、世界音樂與歷史錄音進口商，附門市。2014 年名單另列民生西路 16 號 6 樓之 3，關係不詳。", "Windsong"),
    S("republic", "唱片共和國搖滾專賣店", "indie", "台北市中正區許昌街26號3樓", 2010, "b", 2020, "u", [66, 67, 90],
      "台北車站附近的搖滾與金屬二手店；2010 年已有部落客造訪。"),
    S("chaodai", "朝代音樂", "indie", "台北市萬華區西寧南路36號（獅子林大樓C區）", 2014, "b", 2014, "u", [66],
      "只出現在 2014 年的名單中。", geo="台北市萬華區西寧南路36號"),
    S("stoplisten", "停看聽唱片（八德路）", "indie", "台北市大安區八德路二段18號", 1993, "a", 2017, "e", [75, 76, 66, 90],
      "影音器材行兼賣 CD、黑膠與影碟；2017 年 6 月搬離光華商圈。"),
    S("stoplisten2", "停看聽唱片（重慶北路）", "indie", "台北市大同區重慶北路二段74號12樓", 2017, "e", 2020, "u", [102, 90],
      "嘉慶大樓 12 樓，上樓前要先告知管理員；之後公司登記在內湖，近況不詳。"),
    S("regen-station", "再生工場 站前店", "indie", "台北市中正區許昌街12號2樓", 2014, "b", 2023, "u", [66, 67, 85, 84, 90],
      "二手 CD 起家的連鎖二手店；2023 年仍在許昌街，後來搬到新北永和。"),
    S("taiwane", "台灣ê店", "indie", "台北市大安區新生南路三段76巷6號1樓", 1993, "e", 2022, "e", [81, 66, 90],
      "以台灣研究書籍為主，兼賣台語與原住民音樂 CD；2022 年初租約到期遷出。"),
    S("thokphai", "讀派（台灣ê店遷址）", "indie", "台北市中正區鎮江街1巷3號1樓", 2022, "e", 2024, "e", [81],
      "2022 年 5 月 14 日開幕，2024 年 1 月底結束。"),
    S("seedtoss", "SEED TOSS", "indie", "台北市中正區羅斯福路三段244巷10弄2號B1", 2013, "e", 2015, "e", [82, 66],
      "與漫畫店 Mangasick 同一個地下室的獨立唱片行，2015 年 6 月宣布結束實體營業。"),
    S("agnesb", "agnès b. music store", "indie", "台北市信義區松高路16號2樓（微風松高）", 2014, "e", 2017, "e", [79, 80, 66, 90, 123],
      "agnès b. 全球第二家唱片行，2014 年冬天開幕，營業到 2017 年。", geo="台北市信義區松高路16號"),
    S("kaeru", "KAERU", "indie", "台北市大安區忠孝東路三段248巷15號1樓", 2026, "e", None, None, [124, 123],
      "中古與全新黑膠、唱盤與音響，以爵士、日本 City Pop、靈魂樂為主。先以網路商店營運，實體店預計 2026 年底開幕；店址為官網的聯絡地址。"),
    # ---- 2000 年普查、2020 清單與製作者提供的線索 ----
    S("play", "Play 唱片走廊", "indie", "台北市大安區忠孝東路四段97號（頂好名店城4樓）", 1998, "e", 2000, "u", [95, 57],
      "黃子佼 1998 年 6 月開的唱片行，狹長如走廊，賣港、日、韓 CD、雜誌與周邊；2000 年仍營業，歇業年不詳。門牌依頂好名店城位置。",
      geo="台北市大安區忠孝東路四段97號"),
    S("twave-zx", "T-Wave 忠孝店", "chain", "台北市中正區忠孝東路一段54號", 2000, "e", 2004, "u", [93, 94],
      "T-ZONE 電腦賣場與日本 WAVE 合作的唱片部門，2000 年 5 月起陸續開設；2004 年 4 月的清單仍列出。"),
    S("twave-hp", "T-Wave 和平店", "chain", "台北市中正區羅斯福路二段100號", 2000, "e", 2004, "u", [93, 94],
      "T-ZONE 和平店一樓與地下樓；2004 年 4 月的清單仍列出。"),
    S("eslite-r79", "誠品音樂 R79", "chain", "台北市大同區南京西路16號B1（中山地下書街）", 2017, "e", 2020, "u", [98, 90],
      "2017 年 8 月開幕，有 80 年代主題的黑膠唱片區；2020 年清單仍列出，近況未證實。", "Eslite", geo="台北市大同區南京西路16號"),
    S("wind-huashan", "風潮音樂 華山店", "chain", "台北市中正區八德路一段1號（華山1914）", 2013, "e", 2020, "u", [99, 90],
      "風潮唱片 2013 年在華山開的約 65 坪旗艦店；2020 年清單仍列出。", "Wind Music", geo="台北市中正區八德路一段1號"),
    S("wind-ntch", "風潮音樂 兩廳院店", "chain", "台北市中正區中山南路21-1號（國家音樂廳）", 2015, "b", 2021, "a", [143, 144, 90],
      "國家音樂廳的駐店，2015 年 10 月已在兩廳院駐店名單上（應在小閔的古典音樂世界 2014 年底結束之後進駐）；2020 年 7 月名單仍列出，2022 年 12 月已無，結束時間約在 2021 年前後。", "Wind Music", geo="台北市中正區中山南路21-1號"),
    S("fnac-a9", "法雅客 信義店", "chain", "台北市信義區松壽路9號B2（新光三越 A9）", 2003, "a", 2020, "u", [100, 90],
      "2003 年新光三越與 Fnac 合資開設；2020 年清單仍列為唱片行，現在的法雅客已不賣音樂。", "FNAC", geo="台北市信義區松壽路9號"),
    S("acdc", "越點專業音響", "indie", "台北市大安區和平東路二段345-1號", 2009, "e", None, None, [101, 90],
      "1978 年起在和平東路北教大對面經營的音響店，2009 年 6 月搬到現址，兼賣 LP 與 CD。", "Audio Climax"),
    S("findmemory", "尋找回憶", "indie", "台北市大同區甘州街46號", 2020, "b", None, None, [90], "只出現在 2020 年的清單中。"),
    S("mollie2", "茉莉二手書店 影音館（244巷）", "indie", "台北市中正區羅斯福路三段244巷10弄17號", 2020, "b", None, None, [90],
      "茉莉影音館在 2020 年清單上的地址，搬遷年不詳。"),
]

EVENTS = [
    dict(y=2000, t="羅悅全《秘密基地》把台北唱片行分成四區：東區頂好（東淘、Play 唱片走廊、M@M）、西門町與車站前（西淘、佳佳、九五、ABCD、大眾、玫瑰、光南）、公館（誠品音樂館、大眾、玫瑰、宇宙城、個體戶）、光華與中山北路（光華、合友、FNAC、傑笙）。T-Wave 5 月開幕。"),
    dict(y=2007, t="玫瑰站前（公園路）、民生、公館三家店在上半年先後歇業；玫瑰 1987 年正是從公館起家。"),
    dict(y=2001, t="玫瑰唱片官網的門市表顯示，這年玫瑰在台北市有 10 家店：許昌、光復、民生三店新開幕，公館 142 號老店與汀州路的音樂 99 歇業。大眾唱片則有 6 家。"),
    dict(y=2002, t="6 月，玫瑰唱片與大眾唱片合併為玫瑰大眾，7 月的官網寫著「全省大眾玫瑰 47 家門市」，合併後最多時全台有 52 家。誠品音樂館約在這年從台大移到敦南。"),
    dict(y=2004, t="五大唱片 7 月租下西寧南路 58 號，在西門町開店。"),
    dict(y=2003, t="11 月，淘兒唱片退出台灣，頂好、西門、天母、信義四家店結束前曾五折清倉。玫瑰 2002 年 6 月到 2005 年 11 月之間的門市表沒有存檔，這段期間有幾家店的結束時間只能估計。"),
    dict(y=2006, t="玫瑰峨嵋店、天母店與特易購三民店在上半年歇業。1 月 29 日光華橋與光華商場拆除，攤商移到臨時商場。"),
    dict(y=2008, t="7 月光華數位新天地開幕，原光華商場攤商進駐。"),
    dict(y=2009, t="玫瑰忠孝（頂好）店春天歇業，年底在信義威秀與微風廣場開出新店。五大唱片接手頂好門市，同一地址先後是淘兒、玫瑰、五大；小白兔 7 月在師大浦城街開店。"),
    dict(y=2013, t="玫瑰通化店下半年歇業，此後台北市沒有以玫瑰為名的門市。這年的網路唱片店名單補進一批開業年不詳的店（二手店、連鎖分店），曲線上升有一部分來自資料。"),
    dict(y=2011, t="玫瑰威秀、微風與加州西門店在 7–10 月間歇業，台北市掛玫瑰招牌的只剩通化店。"),
    dict(y=2012, t="1 月小白兔 The Wall 店歇業；大眾唱片台大店 3 月傳出將結束，年底歇業。"),
    dict(y=2014, t="這年新開幕的店特別多：沒有新歌的唱片行、貳樂號 2manyminds、BEANS & BEATS、Vinyl Decision、先行一車、agnès b. music store、新天新地 2。"),
    dict(y=2015, t="Waiting Room 從泰順街搬到中山；風和日麗唱片行在和平東路開店。"),
    dict(y=2019, t="風和日麗唱片行 12 月 1 日歇業；M@M Records 在原址重新開幕。"),
    dict(y=2016, t="玫瑰大眾台中新時代店歇業後，全台只剩台北的古典館。"),
    dict(y=2020, t="5 月 31 日誠品敦南店歇業，地下樓的音樂館一起結束；五大頂好店也在這年歇業。"),
    dict(y=2023, t="12 月 24 日誠品信義店歇業，店內的音樂館隨之結束。K-MONSTAR 在赤峰街開出在台第一家門市，之後赤峰街陸續聚集多家韓國流行專輯店。"),
    dict(y=2022, t="9 月大韜黑膠北流店在台北流行音樂中心對面開幕，號稱全台最大黑膠店。"),
    dict(y=2024, t="誠品 24 小時音樂館移到松菸；THT 搬到松山擴大為黑膠音樂圖書館；五大搬到南陽街；沒有新歌的唱片行結束實體店。"),
    dict(y=2025, t="8 月摔碟唱片舍在大安區巷弄開幕。"),
    dict(y=2026, t="玫瑰大眾古典館 11 月 30 日結束營業，玫瑰大眾從此不再有實體門市。這年的文化部與 Record Store Day 店家名單補進一批開業年不詳的現存店家（含多家韓國流行專輯店），曲線末端上揚有一部分來自資料。"),
]

# Same shop at a new address (or renamed in place): (old id, new id).
# The page treats the chain as one shop: counted once in the move year, founding year taken from the first link.
MOVES = [
    ("eslite-ntu", "eslite-dunnan"),
    ("rose-ufo", "rose-dinghao"),
    ("rose-tongh0", "rose-tongh"),
    ("tachung-xuchang", "rose-chongqing"),
    ("5music-ximen1", "5music-ximen2"),
    ("5music-xuchang", "5music-station"),
    ("knn-xuchang0", "knn-xuchang"),
    ("chiachia-zx", "lele"),
    ("qianwei0", "qianwei"),
    ("jiesheng0", "jiesheng"),
    ("hoyou0", "hoyou"),
    ("cosmos", "rose-music99"),
    ("chiachia-hankou0", "chiachia-hankou"),
    ("rk0", "rk"),
    ("rk", "rk2"),
    ("mollie", "mollie2"),
    ("tht1", "tht2"),
    ("waiting0", "waiting"),
    ("vinyldecision1", "vinyldecision2"),
    ("2manyminds0", "2manyminds"),
    ("xiaosong1", "xiaosong"),
    ("xintianxindi", "xintianxindi2"),
    ("xintianxindi2", "xintianxindi3"),
    ("impo0", "impo"),
    ("senko1", "senko2"),
    ("fairytree1", "fairytree2"),
    ("stoplisten", "stoplisten2"),
    ("candle0", "candle1"),
    ("candle1", "candle"),
    ("abcd", "rose-emei"),
]
# Founding year when the earlier address is not on the map (before 2000 or outside Taipei City).
EST = {"chiachia-zhonghua": (1976, "e", "中華商場"), "acdc": (1978, "e", "和平東路")}

_by = {s["id"]: s for s in STORES}
for a, b in MOVES:
    assert a in _by and b in _by, (a, b)
    assert "prev" not in _by[b] and "next" not in _by[a], (a, b)
    _by[b]["prev"] = a
    _by[a]["next"] = b
for k, (y, q, where) in EST.items():
    _by[k]["est"] = dict(y=y, q=q, at=where)

# Licensed photos (Wikimedia Commons), shown in the shop card with credit.
PHOTOS = {
    "chiachia-zhonghua": dict(f="photos/chiachia-zhonghua.jpg", by="Solomon203", lic="CC BY-SA 4.0", page="https://commons.wikimedia.org/wiki/File:2F_entrance,_Chia_Chia_Record_Zhonghua_Store_20200718.jpg", date="2020"),
    "95": dict(f="photos/95.jpg", by="Solomon203", lic="CC BY-SA 4.0", page="https://commons.wikimedia.org/wiki/File:95Music_Zone_HQ_open_20220918.jpg", date="2022"),
    "5music-ximen1": dict(f="photos/5music-ximen1.jpg", by="Tianmu peter", lic="CC BY 3.0", page="https://commons.wikimedia.org/wiki/File:Five_Music_Ximen_Store_20080805.jpg", date="2008"),
    "knn-xuchang0": dict(f="photos/knn-xuchang0.jpg", by="Solomon203", lic="CC BY-SA 4.0", page="https://commons.wikimedia.org/wiki/File:Kuang_Nan_Fashion_Shop_Taipei_Xuchang_Store_20210906.jpg", date="2021"),
    "knn-xuchang": dict(f="photos/knn-xuchang.jpg", by="Solomon203", lic="CC BY-SA 4.0", page="https://commons.wikimedia.org/wiki/File:Kuang_Nan_Fashion_Shop_Taipei_Xuchang_Store_20241208.jpg", date="2024"),
    "shangyang": dict(f="photos/shangyang.jpg", by="Solomon203", lic="CC BY-SA 4.0", page="https://commons.wikimedia.org/wiki/File:Sunrise_Records_HQ_20150815.jpg", date="2015"),
}
for k, v in PHOTOS.items():
    _by[k]["photo"] = v

# Shop logos for the map's 招牌 mode. Logos belong to the shops; any shop that objects gets removed (see 資料來源).
# key: (file, credit kind, url or "", store ids: exact id or "<id>-..." family, plate colour behind transparent logos)
#   credit kind: "site" = the shop's or brand's own website, "commons" = Wikimedia Commons public domain,
#                "maker" = supplied by Brien John, "web" = a public image of the shop found online (social pages)
OFFICIAL, COMMONS, MAKER, WEB = "site", "commons", "maker", "web"
LOGOS = {
    "5music": ("logos/5music.png", OFFICIAL, "https://www.5music.com.tw/", ["5music"], "#fff"),
    "acdc": ("logos/acdc.png", OFFICIAL, "https://www.acdc.com.tw/", ["acdc"], "#fff"),
    "agnesb": ("logos/agnesb.svg", OFFICIAL, "https://www.agnesb.com/", ["agnesb"], "#fff"),
    "cheery": ("logos/cheery.png", OFFICIAL, "https://www.cheerymusic.com/", ["cheery"], "#fff"),
    "eslite": ("logos/eslite.png", OFFICIAL, "https://www.eslite.com/", ["eslite"], "#fff"),
    "gmusic": ("logos/gmusic.png", OFFICIAL, "https://www.g-music.com.tw/", ["rose", "tachung"], "#fff"),
    "kaeru": ("logos/kaeru.png", OFFICIAL, "https://www.kaerutw.com/", ["kaeru"], "#fff"),
    "kmonstar": ("logos/kmonstar.png", OFFICIAL, "https://kmonstar.com/", ["kmonstar"], "#fff"),
    "knn": ("logos/knn.png", OFFICIAL, "https://www.knn.com.tw/", ["knn"], "#fff"),
    "mam": ("logos/mam.png", OFFICIAL, "https://www.mmrecords.com.tw/", ["mam", "mam2"], "#141414"),
    "regen": ("logos/regen.png", OFFICIAL, "https://www.shshop.me/", ["regen"], "#fff"),
    "wabbit": ("logos/wabbit.png", OFFICIAL, "https://wwr.com.tw/", ["wabbit"], "#fff"),
    "wind": ("logos/wind.png", OFFICIAL, "https://www.windmusic.com.tw/", ["wind"], "#fff"),
    "rk": ("logos/rk.png", OFFICIAL, "https://www.rkrecord.com.tw/", ["rk", "rk0", "rk2"], "#cacbcc"),
    "soundsgood": ("logos/soundsgood.png", OFFICIAL, "https://soundsgoodtaipei.com.tw/", ["soundsgood"], "#231f20"),
    "chaobar": ("logos/chaobar.png", MAKER, "", ["chaobar"], "#fff"),
    "rotten": ("logos/rotten.png", OFFICIAL, "https://www.rottenblues.com/", ["rotten"], "#000"),
    "willmusic": ("logos/willmusic.png", OFFICIAL, "https://www.willmusic.com.tw/", ["willmusic1", "willmusic2", "willmusic-att", "willmusic-ximen"], "#1d1d1f"),
    "tower": ("logos/tower.svg", COMMONS, "https://commons.wikimedia.org/wiki/File:Tower_Records_logo_vertical.svg", ["tower"], "#ffe000"),
    "fnac": ("logos/fnac.svg", COMMONS, "https://commons.wikimedia.org/wiki/File:Fnac_Logo.svg", ["fnac"], "#fff"),
    "joyaudio": ("logos/joyaudio.png", MAKER, "", ["joyaudio"], "#000"),
    "qiyuan": ("logos/qiyuan.png", MAKER, "", ["qiyuan1", "qiyuan2"], "#7cc242"),
    "hoyou": ("logos/hoyou.png", MAKER, "", ["hoyou", "hoyou0"], "#fff"),
    "95": ("logos/95.png", MAKER, "", ["95"], "#fff"),
    "38c": ("logos/38c.png", MAKER, "", ["38c"], "#6d1d2e"),
    "shangyang": ("logos/shangyang.png", MAKER, "", ["shangyang"], "#fff"),
    "chiachia": ("logos/chiachia.png", WEB, "", ["chiachia"], "#f7f7f7"),
    "indimusic": ("logos/indimusic.png", WEB, "", ["indimusic"], "#000"),
    "waiting": ("logos/waiting.png", WEB, "", ["waiting", "waiting0"], "#fff"),
    "tht": ("logos/tht.png", WEB, "", ["tht1", "tht2", "tht-room25"], "#f7f7f7"),
    "senko": ("logos/senko.png", WEB, "", ["senko1", "senko2"], "#000"),
    "vinyldecision": ("logos/vinyldecision.png", WEB, "", ["vinyldecision1", "vinyldecision2"], "#f3eee2"),
    "slipped": ("logos/slipped.png", WEB, "", ["slipped"], "#1c4e91"),
    "mollie": ("logos/mollie.png", WEB, "", ["mollie", "mollie2"], "#000"),
    "btb": ("logos/btb.png", WEB, "", ["btb"], "#f7f7f7"),
    "agoodday": ("logos/agoodday.png", WEB, "", ["agoodday"], "#29a8e0"),
    "syntrend": ("logos/syntrend.png", WEB, "", ["syntrend"], "#fff"),
    "datao": ("logos/datao.png", WEB, "", ["datao"], "#f7f7f7"),
    "windsong": ("logos/windsong.png", OFFICIAL, "http://www.windsong.com.tw/", ["windsong"], "#fff"),
    "xiaosong": ("logos/xiaosong.png", MAKER, "", ["xiaosong", "xiaosong1"], "#1e6b1e"),
    "soulamazin": ("logos/soulamazin.png", MAKER, "", ["soulamazin"], "#ffe000"),
    "pubmetal": ("logos/pubmetal.png", MAKER, "", ["pubmetal"], "#fff"),
    "sidoli": ("logos/sidoli.png", MAKER, "", ["sidoli"], "#fff"),
    "aile": ("logos/aile.png", MAKER, "", ["aile1", "aile2"], "#f5f5f7"),
    "seedtoss": ("logos/seedtoss.png", MAKER, "", ["seedtoss"], "#fff"),
    "beansbeats": ("logos/beansbeats.png", MAKER, "", ["beansbeats"], "#6b3a2e"),
    "2manyminds": ("logos/2manyminds.png", MAKER, "", ["2manyminds0", "2manyminds"], "#fff"),
    "xiaomin": ("logos/xiaomin.png", MAKER, "", ["xiaomin"], "#2a2118"),
    "candle": ("logos/candle.png", MAKER, "", ["candle", "candle0", "candle1"], "#fff"),
    "parstore": ("logos/parstore.png", MAKER, "", ["parstore"], "#fff"),
    "analogy": ("logos/analogy.png", MAKER, "", ["analogy"], "#e3cfb4"),
    "blackglue": ("logos/blackglue.png", MAKER, "", ["blackglue"], "#fff"),
    "avc": ("logos/avc.png", MAKER, "", ["avc"], "#fff"),
    "allmyday": ("logos/allmyday.png", MAKER, "", ["allmyday1", "allmyday2"], "#fff"),
    "koreepop": ("logos/koreepop.png", MAKER, "", ["koreepop"], "#fff"),
    "fairytree": ("logos/fairytree.png", MAKER, "", ["fairytree1", "fairytree2"], "#fff"),
    "hanju": ("logos/hanju.png", MAKER, "", ["hanju", "hanju2"], "#fff"),
    "taiwane": ("logos/taiwane.png", MAKER, "", ["taiwane"], "#d8ecd0"),
    "thokphai": ("logos/thokphai.png", MAKER, "", ["thokphai"], "#4a1c25"),
    "dalangman": ("logos/dalangman.png", MAKER, "", ["dalangman"], "#fff"),
    "ygm": ("logos/ygm.png", MAKER, "", ["ygm"], "#fff"),
}
import struct, re as _re
def _dims(path):
    full = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", path)
    if path.endswith(".svg"):
        vb = _re.search(r'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', open(full, encoding="utf-8").read())
        return float(vb.group(1)), float(vb.group(2))
    with open(full, "rb") as fh:
        head = fh.read(24)
    return struct.unpack(">II", head[16:24])
for key, (f, kind, u, fams, bg) in LOGOS.items():
    w, h = _dims(f)
    hit = [s for s in STORES if any(s["id"] == p or s["id"].startswith(p + "-") for p in fams)]
    assert hit, key
    for s in hit:
        s["logo"] = dict(f=f, k=kind, u=u, bg=bg, a=round(w / h, 3))

out = dict(sources=[dict(t=t, u=u) for t, u in SOURCES], zones=ZONES, stores=STORES, events=EVENTS)
ids = [s["id"] for s in STORES]
assert len(ids) == len(set(ids)), "duplicate id"
for s in STORES:
    assert all(0 <= i < len(SOURCES) for i in s["src"]), s["id"]
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "stores.json"), "w"), ensure_ascii=False, indent=1)
print(len(STORES), "stores")
