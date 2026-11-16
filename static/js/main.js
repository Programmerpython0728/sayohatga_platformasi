/* =============================================
   SAYOHATGA — MAIN JAVASCRIPT
   ============================================= */
'use strict';

// ─── TRANSLATIONS ───────────────────────────────────────────────────────────
const TRANSLATIONS = {
  uz: {
    // Nav
    nav_places:       "Joylar",
    nav_stays:        "Turar joylar",
    nav_basket:       "Savatcha",
    nav_cabinet:      "Kabinet",
    nav_profile:      "Profil",
    nav_login:        "Kirish",
    nav_register:     "Ro'yxatdan o'tish",
    nav_logout:       "Chiqish",
    // Hero
    hero1_label:      "🇺🇿 O'zbekiston Turizmi",
    hero1_title:      "O'zbekistonni <span class='accent'>kashf eting</span>",
    hero1_desc:       "Samarqand, Buxoro, Xiva va boshqa go'zal joylarga sayohat qiling. Premium xizmat, qulay narxlar.",
    hero2_label:      "⚡ Tez Bron",
    hero2_title:      "Navbatsiz <span class='accent'>bron qiling</span>",
    hero2_desc:       "Mehmonxona, dacha va resortlarni bir necha soniyada bron qiling. Hech qanday ortiqcha to'lov yo'q.",
    hero3_label:      "📱 Telegram OTP",
    hero3_title:      "Telegram orqali <span class='accent'>tez tasdiqlash</span>",
    hero3_desc:       "Shaxsingizni Telegram bot orqali tasdiqlang. Xavfsiz, tez va qulay ro'yxatdan o'tish.",
    hero_btn_places:  "Joylarni ko'rish",
    hero_btn_stays:   "Turar joy topish",
    hero_btn_register:"Ro'yxatdan o'tish",
    hero_btn_how:     "Qanday ishlaydi",
    hero_stat1_num:   "1200+",
    hero_stat1_lbl:   "Turistik joylar",
    hero_stat2_num:   "850+",
    hero_stat2_lbl:   "Turar joylar",
    hero_stat3_num:   "15K+",
    hero_stat3_lbl:   "Foydalanuvchilar",
    hero_stat4_num:   "4.9★",
    hero_stat4_lbl:   "O'rtacha baho",
    // Sections
    sec_popular_label:"Mashhur joylar",
    sec_popular_h2:   "Ko'p tashrif buyurilgan joylar",
    sec_popular_p:    "O'zbekistonning eng go'zal va tarixiy joylarini kashf eting",
    sec_stays_label:  "Top turar joylar",
    sec_stays_h2:     "Premium mehmonxona va dachalar",
    sec_stays_p:      "Eng yaxshi turar joylarni qidiring va bron qiling",
    sec_why_label:    "Nima uchun biz?",
    sec_why_h2:       "Sayohatga bilan qanday foydalar bor?",
    sec_how_label:    "Qanday ishlaydi",
    sec_how_h2:       "Bron qilish juda oson",
    see_all:          "Hammasini ko'rish",
    view_info:        "Batafsil",
    book_now:         "Bron qilish",
    add_basket:       "Savatchaga",
    // Cards
    per_night:        "/ kecha",
    guests:           "mehmon",
    // Why
    why1_title:       "Ishonchli platforma",
    why1_desc:        "Barcha turar joylar tekshirilgan va sertifikatlangan",
    why2_title:       "Qulay narxlar",
    why2_desc:        "Bozordagi eng yaxshi narxlarni taklif etamiz",
    why3_title:       "Tez javob",
    why3_desc:        "24/7 qo'llab-quvvatlash va tez bron tasdiqlash",
    why4_title:       "Telegram login",
    why4_desc:        "Xavfsiz Telegram OTP orqali tizimga kiring",
    why5_title:       "3 tilda",
    why5_desc:        "UZ, RU, EN tillarida to'liq qo'llab-quvvatlash",
    why6_title:       "Mobil qulay",
    why6_desc:        "Har qanday qurilmada mukammal ishlaydi",
    // Steps
    step1_title:      "Ro'yxatdan o'ting",
    step1_desc:       "Telegram bot orqali tez va oson ro'yxatdan o'ting",
    step2_title:      "Joy tanlang",
    step2_desc:       "Minglab joylar va turar joylardan eng yaxshisini tanlang",
    step3_title:      "Bron yuboring",
    step3_desc:       "Sanalarni kiriting va bron so'rovini yuboring",
    step4_title:      "Tasdiqlaning",
    step4_desc:       "Admin tasdiqlaydi va siz xabar olasiz",
    // CTA Band
    cta_title:        "Bugun sayohatingizni boshlang!",
    cta_desc:         "O'zbekistonning eng go'zal joylarini kashf eting. Ro'yxatdan o'tish bepul va tez.",
    cta_btn1:         "Bepul ro'yxatdan o'tish",
    cta_btn2:         "Joylarni ko'rish",
    // List pages
    places_title:     "Turistik joylar",
    places_desc:      "O'zbekistonning go'zal turistik joylarini kashf eting",
    stays_title:      "Turar joylar",
    stays_desc:       "Mehmonxona, dacha va resortlarni qidiring",
    search_ph:        "Qidirish...",
    filter_region:    "Viloyat",
    filter_city:      "Shahar",
    filter_type:      "Turi",
    filter_min_price: "Min narx",
    filter_max_price: "Max narx",
    filter_btn:       "Filter",
    all_regions:      "Barcha viloyatlar",
    all_cities:       "Barcha shaharlar",
    all_types:        "Barcha turlar",
    no_results:       "Natija topilmadi",
    no_results_desc:  "Boshqa kalit so'z yoki filter sinab ko'ring",
    // Detail
    nearby_stays:     "Yaqin turar joylar",
    reviews:          "Sharhlar",
    no_reviews:       "Hali sharh yo'q",
    // Basket
    basket_title:     "Savatcha",
    basket_empty:     "Savatcha bo'sh",
    basket_empty_desc:"Sevimli joylarni savatchaga qo'shing",
    basket_explore_p: "Joylarni ko'rish",
    basket_explore_s: "Turar joylarni ko'rish",
    remove:           "O'chirish",
    // Login
    login_title:      "Kirish",
    login_subtitle:   "Hisobingizga kiring",
    login_phone:      "Telefon raqam",
    login_password:   "Parol",
    login_btn:        "Kirish",
    login_or:         "yoki",
    login_tg_title:   "Telegram orqali kirish",
    login_tg_desc:    "Telegram botdan OTP kod oling va kirish qiling",
    login_tg_step:    "Telegram botni ochish",
    login_otp:        "OTP kod",
    login_tg_btn:     "Telegram OTP bilan kirish",
    login_no_acc:     "Hisobingiz yo'qmi?",
    login_register:   "Ro'yxatdan o'tish",
    // Register
    reg_title:        "Ro'yxatdan o'tish",
    reg_subtitle:     "Yangi hisob yarating",
    reg_phone:        "Telefon raqam",
    reg_fullname:     "To'liq ism",
    reg_password:     "Parol",
    reg_password2:    "Parolni takrorlash",
    reg_otp:          "Telegram OTP kod",
    reg_tg_hint:      "Telegram botdan OTP oling",
    reg_open_tg:      "Telegram botni ochish",
    reg_btn:          "Ro'yxatdan o'tish",
    reg_has_acc:      "Hisobingiz bormi?",
    reg_login:        "Kirish",
    // OTP Help
    otp_title:        "Telegram orqali tasdiqlash",
    otp_intro:        "OTP kodni qanday olish kerak?",
    otp_step1:        "Telegram botni oching",
    otp_step1_desc:   "Quyidagi tugmani bosib Telegram botimizni oching",
    otp_step2:        "/start buyrug'ini yuboring",
    otp_step2_desc:   "Botga /start yozing yoki Start tugmasini bosing",
    otp_step3:        "OTP kodni oling",
    otp_step3_desc:   "Bot sizga 6 xonali tasdiqlash kodini yuboradi",
    otp_step4:        "Kodni kiriting",
    otp_step4_desc:   "Olingan kodni ro'yxatdan o'tish formasiga kiriting",
    otp_open_bot:     "Telegram botni ochish",
    otp_tip:          "💡 Maslahat: Kod 10 daqiqa davomida amal qiladi",
    otp_go_reg:       "Ro'yxatdan o'tishga o'tish",
    otp_go_login:     "Kirish sahifasiga o'tish",
    // Booking
    book_title:       "Bron yaratish",
    book_date_from:   "Kelish sanasi",
    book_date_to:     "Ketish sanasi",
    book_guests:      "Mehmonlar soni",
    book_send:        "So'rov yuborish",
    book_back:        "Orqaga",
    book_login_hint:  "Bron qilish uchun tizimga kiring",
    // Dashboard
    dash_bookings:    "Bronlarim",
    dash_liked_p:     "Sevimli joylar",
    dash_liked_s:     "Sevimli turar joylar",
    dash_quick:       "Tezkor havolalar",
    dash_no_book:     "Bronlar yo'q",
    dash_no_liked:    "Sevimlilarga hech narsa qo'shilmagan",
    dash_cancel:      "Bekor qilish",
    // Profile
    prof_title:       "Profil",
    prof_phone:       "Telefon",
    prof_name:        "To'liq ism",
    prof_email:       "Email",
    prof_status:      "Holat",
    prof_since:       "A'zo bo'lgan sana",
    prof_edit:        "Tahrirlash",
    prof_save:        "Saqlash",
    // Footer
    footer_about:     "Biz haqimizda",
    footer_about_desc:"Sayohatga — O'zbekiston bo'yicha eng qulay turistik platforma. Joylar, turar joylar va bron bir joyda.",
    footer_links:     "Foydali havolalar",
    footer_contact:   "Kontakt",
    footer_social:    "Ijtimoiy tarmoqlar",
    footer_tg:        "Telegram botni ochish",
    footer_copy:      "© 2025 Sayohatga. Barcha huquqlar himoyalangan.",
    // General
    active:           "Faol",
    pending:          "Kutilmoqda",
    confirmed:        "Tasdiqlangan",
    canceled:         "Bekor qilingan",
    loading:          "Yuklanmoqda...",
    error_generic:    "Xatolik yuz berdi",
    success_like:     "Sevimlilarga qo'shildi",
    success_basket:   "Savatchaga qo'shildi",
    removed_basket:   "Savatchadan o'chirildi",
  },
  ru: {
    nav_places:       "Места",
    nav_stays:        "Жильё",
    nav_basket:       "Корзина",
    nav_cabinet:      "Кабинет",
    nav_profile:      "Профиль",
    nav_login:        "Войти",
    nav_register:     "Регистрация",
    nav_logout:       "Выйти",
    hero1_label:      "🇺🇿 Туризм Узбекистана",
    hero1_title:      "Откройте для себя <span class='accent'>Узбекистан</span>",
    hero1_desc:       "Путешествуйте в Самарканд, Бухару, Хиву и другие красивые места. Премиум сервис, доступные цены.",
    hero2_label:      "⚡ Быстрое бронирование",
    hero2_title:      "Бронируйте <span class='accent'>без очереди</span>",
    hero2_desc:       "Бронируйте отели, дачи и курорты за несколько секунд. Никаких скрытых платежей.",
    hero3_label:      "📱 Telegram OTP",
    hero3_title:      "Быстрое подтверждение <span class='accent'>через Telegram</span>",
    hero3_desc:       "Подтвердите личность через Telegram-бот. Безопасная и удобная регистрация.",
    hero_btn_places:  "Смотреть места",
    hero_btn_stays:   "Найти жильё",
    hero_btn_register:"Регистрация",
    hero_btn_how:     "Как это работает",
    hero_stat1_num:   "1200+",
    hero_stat1_lbl:   "Туристических мест",
    hero_stat2_num:   "850+",
    hero_stat2_lbl:   "Вариантов жилья",
    hero_stat3_num:   "15K+",
    hero_stat3_lbl:   "Пользователей",
    hero_stat4_num:   "4.9★",
    hero_stat4_lbl:   "Средний рейтинг",
    sec_popular_label:"Популярные места",
    sec_popular_h2:   "Часто посещаемые места",
    sec_popular_p:    "Откройте самые красивые исторические места Узбекистана",
    sec_stays_label:  "Топ жильё",
    sec_stays_h2:     "Премиум отели и дачи",
    sec_stays_p:      "Найдите и забронируйте лучшее жильё",
    sec_why_label:    "Почему мы?",
    sec_why_h2:       "Преимущества Sayohatga",
    sec_how_label:    "Как это работает",
    sec_how_h2:       "Бронирование — это просто",
    see_all:          "Смотреть все",
    view_info:        "Подробнее",
    book_now:         "Забронировать",
    add_basket:       "В корзину",
    per_night:        "/ ночь",
    guests:           "гостей",
    why1_title:       "Надёжная платформа",
    why1_desc:        "Все объекты проверены и сертифицированы",
    why2_title:       "Выгодные цены",
    why2_desc:        "Предлагаем лучшие цены на рынке",
    why3_title:       "Быстрый ответ",
    why3_desc:        "Поддержка 24/7 и быстрое подтверждение",
    why4_title:       "Telegram-вход",
    why4_desc:        "Безопасный вход через Telegram OTP",
    why5_title:       "3 языка",
    why5_desc:        "Полная поддержка UZ, RU, EN",
    why6_title:       "Мобильный",
    why6_desc:        "Отлично работает на любом устройстве",
    step1_title:      "Зарегистрируйтесь",
    step1_desc:       "Быстрая регистрация через Telegram-бот",
    step2_title:      "Выберите место",
    step2_desc:       "Выберите лучшее из тысяч вариантов",
    step3_title:      "Отправьте запрос",
    step3_desc:       "Введите даты и отправьте запрос",
    step4_title:      "Получите подтверждение",
    step4_desc:       "Администратор подтвердит и вы получите уведомление",
    cta_title:        "Начните путешествие сегодня!",
    cta_desc:         "Откройте красивейшие места Узбекистана. Регистрация бесплатна.",
    cta_btn1:         "Зарегистрироваться бесплатно",
    cta_btn2:         "Смотреть места",
    places_title:     "Туристические места",
    places_desc:      "Откройте красивые туристические места Узбекистана",
    stays_title:      "Варианты жилья",
    stays_desc:       "Ищите отели, дачи и курорты",
    search_ph:        "Поиск...",
    filter_region:    "Область",
    filter_city:      "Город",
    filter_type:      "Тип",
    filter_min_price: "Мин. цена",
    filter_max_price: "Макс. цена",
    filter_btn:       "Фильтр",
    all_regions:      "Все области",
    all_cities:       "Все города",
    all_types:        "Все типы",
    no_results:       "Результаты не найдены",
    no_results_desc:  "Попробуйте другое слово или фильтр",
    nearby_stays:     "Ближайшее жильё",
    reviews:          "Отзывы",
    no_reviews:       "Отзывов пока нет",
    basket_title:     "Корзина",
    basket_empty:     "Корзина пуста",
    basket_empty_desc:"Добавьте любимые места в корзину",
    basket_explore_p: "Смотреть места",
    basket_explore_s: "Смотреть жильё",
    remove:           "Удалить",
    login_title:      "Вход",
    login_subtitle:   "Войдите в аккаунт",
    login_phone:      "Номер телефона",
    login_password:   "Пароль",
    login_btn:        "Войти",
    login_or:         "или",
    login_tg_title:   "Вход через Telegram",
    login_tg_desc:    "Получите OTP-код в Telegram-боте",
    login_tg_step:    "Открыть Telegram-бот",
    login_otp:        "OTP-код",
    login_tg_btn:     "Войти через Telegram OTP",
    login_no_acc:     "Нет аккаунта?",
    login_register:   "Зарегистрироваться",
    reg_title:        "Регистрация",
    reg_subtitle:     "Создайте новый аккаунт",
    reg_phone:        "Номер телефона",
    reg_fullname:     "Полное имя",
    reg_password:     "Пароль",
    reg_password2:    "Повторите пароль",
    reg_otp:          "Telegram OTP-код",
    reg_tg_hint:      "Получите OTP из Telegram-бота",
    reg_open_tg:      "Открыть Telegram-бот",
    reg_btn:          "Зарегистрироваться",
    reg_has_acc:      "Уже есть аккаунт?",
    reg_login:        "Войти",
    otp_title:        "Подтверждение через Telegram",
    otp_intro:        "Как получить OTP-код?",
    otp_step1:        "Откройте Telegram-бот",
    otp_step1_desc:   "Нажмите кнопку ниже чтобы открыть наш бот",
    otp_step2:        "Отправьте /start",
    otp_step2_desc:   "Напишите /start или нажмите Start",
    otp_step3:        "Получите OTP-код",
    otp_step3_desc:   "Бот отправит 6-значный код подтверждения",
    otp_step4:        "Введите код",
    otp_step4_desc:   "Введите полученный код в форму регистрации",
    otp_open_bot:     "Открыть Telegram-бот",
    otp_tip:          "💡 Подсказка: Код действителен 10 минут",
    otp_go_reg:       "Перейти к регистрации",
    otp_go_login:     "Перейти ко входу",
    book_title:       "Создать бронирование",
    book_date_from:   "Дата заезда",
    book_date_to:     "Дата выезда",
    book_guests:      "Количество гостей",
    book_send:        "Отправить запрос",
    book_back:        "Назад",
    book_login_hint:  "Войдите для бронирования",
    dash_bookings:    "Мои бронирования",
    dash_liked_p:     "Избранные места",
    dash_liked_s:     "Избранное жильё",
    dash_quick:       "Быстрые ссылки",
    dash_no_book:     "Бронирований нет",
    dash_no_liked:    "Избранное пусто",
    dash_cancel:      "Отменить",
    prof_title:       "Профиль",
    prof_phone:       "Телефон",
    prof_name:        "Полное имя",
    prof_email:       "Email",
    prof_status:      "Статус",
    prof_since:       "Дата регистрации",
    prof_edit:        "Редактировать",
    prof_save:        "Сохранить",
    footer_about:     "О нас",
    footer_about_desc:"Sayohatga — удобная туристическая платформа по всему Узбекистану. Места, жильё и бронирование в одном месте.",
    footer_links:     "Полезные ссылки",
    footer_contact:   "Контакты",
    footer_social:    "Соцсети",
    footer_tg:        "Открыть Telegram-бот",
    footer_copy:      "© 2025 Sayohatga. Все права защищены.",
    active:           "Активен",
    pending:          "Ожидает",
    confirmed:        "Подтверждён",
    canceled:         "Отменён",
    loading:          "Загрузка...",
    error_generic:    "Произошла ошибка",
    success_like:     "Добавлено в избранное",
    success_basket:   "Добавлено в корзину",
    removed_basket:   "Удалено из корзины",
  },
  en: {
    nav_places:       "Places",
    nav_stays:        "Stays",
    nav_basket:       "Basket",
    nav_cabinet:      "Cabinet",
    nav_profile:      "Profile",
    nav_login:        "Sign In",
    nav_register:     "Register",
    nav_logout:       "Sign Out",
    hero1_label:      "🇺🇿 Uzbekistan Tourism",
    hero1_title:      "<span class='accent'>Discover</span> Uzbekistan",
    hero1_desc:       "Travel to Samarkand, Bukhara, Khiva and other beautiful destinations. Premium service, fair prices.",
    hero2_label:      "⚡ Fast Booking",
    hero2_title:      "Book <span class='accent'>without waiting</span>",
    hero2_desc:       "Reserve hotels, villas and resorts in seconds. No hidden fees or extra charges.",
    hero3_label:      "📱 Telegram OTP",
    hero3_title:      "Quick verification <span class='accent'>via Telegram</span>",
    hero3_desc:       "Verify your identity through our Telegram bot. Safe, fast, and convenient registration.",
    hero_btn_places:  "Explore Places",
    hero_btn_stays:   "Find Stays",
    hero_btn_register:"Get Started",
    hero_btn_how:     "How it Works",
    hero_stat1_num:   "1200+",
    hero_stat1_lbl:   "Tourist Spots",
    hero_stat2_num:   "850+",
    hero_stat2_lbl:   "Accommodations",
    hero_stat3_num:   "15K+",
    hero_stat3_lbl:   "Users",
    hero_stat4_num:   "4.9★",
    hero_stat4_lbl:   "Average Rating",
    sec_popular_label:"Popular Places",
    sec_popular_h2:   "Most Visited Destinations",
    sec_popular_p:    "Discover the most beautiful and historic places in Uzbekistan",
    sec_stays_label:  "Top Stays",
    sec_stays_h2:     "Premium Hotels & Villas",
    sec_stays_p:      "Find and book the best accommodations",
    sec_why_label:    "Why Us?",
    sec_why_h2:       "Benefits of Sayohatga",
    sec_how_label:    "How it Works",
    sec_how_h2:       "Booking is Simple",
    see_all:          "See All",
    view_info:        "Details",
    book_now:         "Book Now",
    add_basket:       "Add to Basket",
    per_night:        "/ night",
    guests:           "guests",
    why1_title:       "Trusted Platform",
    why1_desc:        "All properties are verified and certified",
    why2_title:       "Great Prices",
    why2_desc:        "We offer the best market prices",
    why3_title:       "Fast Response",
    why3_desc:        "24/7 support and quick booking confirmation",
    why4_title:       "Telegram Login",
    why4_desc:        "Secure login via Telegram OTP",
    why5_title:       "3 Languages",
    why5_desc:        "Full support in UZ, RU, EN",
    why6_title:       "Mobile Ready",
    why6_desc:        "Works perfectly on any device",
    step1_title:      "Register",
    step1_desc:       "Quick and easy registration via Telegram bot",
    step2_title:      "Choose a Place",
    step2_desc:       "Pick the best from thousands of options",
    step3_title:      "Send Request",
    step3_desc:       "Enter your dates and send a booking request",
    step4_title:      "Get Confirmed",
    step4_desc:       "Admin confirms and you receive a notification",
    cta_title:        "Start Your Journey Today!",
    cta_desc:         "Discover the most beautiful places in Uzbekistan. Registration is free and fast.",
    cta_btn1:         "Register for Free",
    cta_btn2:         "Explore Places",
    places_title:     "Tourist Places",
    places_desc:      "Discover beautiful tourist spots across Uzbekistan",
    stays_title:      "Accommodations",
    stays_desc:       "Find hotels, villas and resorts",
    search_ph:        "Search...",
    filter_region:    "Region",
    filter_city:      "City",
    filter_type:      "Type",
    filter_min_price: "Min Price",
    filter_max_price: "Max Price",
    filter_btn:       "Filter",
    all_regions:      "All Regions",
    all_cities:       "All Cities",
    all_types:        "All Types",
    no_results:       "No results found",
    no_results_desc:  "Try a different keyword or filter",
    nearby_stays:     "Nearby Stays",
    reviews:          "Reviews",
    no_reviews:       "No reviews yet",
    basket_title:     "Basket",
    basket_empty:     "Your basket is empty",
    basket_empty_desc:"Add your favourite places to the basket",
    basket_explore_p: "Explore Places",
    basket_explore_s: "Explore Stays",
    remove:           "Remove",
    login_title:      "Sign In",
    login_subtitle:   "Welcome back",
    login_phone:      "Phone Number",
    login_password:   "Password",
    login_btn:        "Sign In",
    login_or:         "or",
    login_tg_title:   "Sign In with Telegram",
    login_tg_desc:    "Get an OTP code from our Telegram bot",
    login_tg_step:    "Open Telegram Bot",
    login_otp:        "OTP Code",
    login_tg_btn:     "Sign In with Telegram OTP",
    login_no_acc:     "Don't have an account?",
    login_register:   "Register",
    reg_title:        "Register",
    reg_subtitle:     "Create a new account",
    reg_phone:        "Phone Number",
    reg_fullname:     "Full Name",
    reg_password:     "Password",
    reg_password2:    "Confirm Password",
    reg_otp:          "Telegram OTP Code",
    reg_tg_hint:      "Get the OTP from Telegram bot",
    reg_open_tg:      "Open Telegram Bot",
    reg_btn:          "Create Account",
    reg_has_acc:      "Already have an account?",
    reg_login:        "Sign In",
    otp_title:        "Telegram Verification",
    otp_intro:        "How to get your OTP code?",
    otp_step1:        "Open Telegram Bot",
    otp_step1_desc:   "Click the button below to open our bot",
    otp_step2:        "Send /start command",
    otp_step2_desc:   "Type /start or tap the Start button",
    otp_step3:        "Receive OTP Code",
    otp_step3_desc:   "The bot will send you a 6-digit verification code",
    otp_step4:        "Enter the Code",
    otp_step4_desc:   "Enter the received code in the registration form",
    otp_open_bot:     "Open Telegram Bot",
    otp_tip:          "💡 Tip: The code is valid for 10 minutes",
    otp_go_reg:       "Go to Registration",
    otp_go_login:     "Go to Sign In",
    book_title:       "Create Booking",
    book_date_from:   "Check-in Date",
    book_date_to:     "Check-out Date",
    book_guests:      "Number of Guests",
    book_send:        "Send Request",
    book_back:        "Back",
    book_login_hint:  "Sign in to make a booking",
    dash_bookings:    "My Bookings",
    dash_liked_p:     "Liked Places",
    dash_liked_s:     "Liked Stays",
    dash_quick:       "Quick Links",
    dash_no_book:     "No bookings yet",
    dash_no_liked:    "Nothing in favourites",
    dash_cancel:      "Cancel",
    prof_title:       "Profile",
    prof_phone:       "Phone",
    prof_name:        "Full Name",
    prof_email:       "Email",
    prof_status:      "Status",
    prof_since:       "Member Since",
    prof_edit:        "Edit",
    prof_save:        "Save",
    footer_about:     "About Us",
    footer_about_desc:"Sayohatga — Uzbekistan's most convenient tourism platform. Places, stays, and bookings in one place.",
    footer_links:     "Useful Links",
    footer_contact:   "Contact",
    footer_social:    "Social Media",
    footer_tg:        "Open Telegram Bot",
    footer_copy:      "© 2025 Sayohatga. All rights reserved.",
    active:           "Active",
    pending:          "Pending",
    confirmed:        "Confirmed",
    canceled:         "Canceled",
    loading:          "Loading...",
    error_generic:    "An error occurred",
    success_like:     "Added to favourites",
    success_basket:   "Added to basket",
    removed_basket:   "Removed from basket",
  }
};

// ─── LANGUAGE MANAGER ───────────────────────────────────────────────────────
const Lang = {
  current: document.documentElement.lang || localStorage.getItem('sayohatga_lang') || 'uz',

  get(key) {
    return TRANSLATIONS[this.current]?.[key] || TRANSLATIONS['uz'][key] || key;
  },

  set(lang) {
    if (!TRANSLATIONS[lang]) return;
    this.current = lang;
    localStorage.setItem('sayohatga_lang', lang);
    this.updateButtons();

    const next = `${window.location.pathname}${window.location.search}${window.location.hash}`;
    const target = `/lang/${lang}/?next=${encodeURIComponent(next)}`;
    window.location.assign(target);
  },

  applyAll() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.dataset.i18n;
      const val = this.get(key);
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.placeholder = val;
      } else {
        el.innerHTML = val;
      }
    });
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      el.title = this.get(el.dataset.i18nTitle);
    });
  },

  updateButtons() {
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.lang === this.current);
    });
  },

  init() {
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.addEventListener('click', () => this.set(btn.dataset.lang));
    });
    this.current = document.documentElement.lang || this.current || 'uz';
    this.applyAll();
    this.updateButtons();
  }
};

// ─── THEME MANAGER ──────────────────────────────────────────────────────────
const Theme = {
  current: localStorage.getItem('sayohatga_theme') || 'light',

  set(theme) {
    this.current = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('sayohatga_theme', theme);
    this.updateIcon();
  },

  toggle() { this.set(this.current === 'dark' ? 'light' : 'dark'); },

  updateIcon() {
    const icons = document.querySelectorAll('.theme-icon');
    icons.forEach(i => {
      i.textContent = this.current === 'dark' ? '☀️' : '🌙';
    });
  },

  init() {
    this.set(this.current); // apply saved
    document.querySelectorAll('.theme-toggle').forEach(btn => {
      btn.addEventListener('click', () => this.toggle());
    });
  }
};

// ─── HEADER ─────────────────────────────────────────────────────────────────
const Header = {
  init() {
    const header = document.querySelector('.site-header');
    if (!header) return;

    // Scroll effect
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 20);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // Hamburger
    const hamburger = document.querySelector('.hamburger');
    const mobileNav = document.querySelector('.mobile-nav');
    if (hamburger && mobileNav) {
      hamburger.addEventListener('click', () => {
        const open = hamburger.classList.toggle('open');
        mobileNav.classList.toggle('open', open);
        document.body.style.overflow = open ? 'hidden' : '';
      });

      // Close on outside click
      document.addEventListener('click', e => {
        if (!header.contains(e.target) && !mobileNav.contains(e.target)) {
          hamburger.classList.remove('open');
          mobileNav.classList.remove('open');
          document.body.style.overflow = '';
        }
      });
    }
  }
};

// ─── HERO CAROUSEL ──────────────────────────────────────────────────────────
const Carousel = {
  el: null,
  slides: [],
  dots: [],
  current: 0,
  timer: null,
  interval: 5500,

  init() {
    this.el = document.querySelector('.hero-slides');
    if (!this.el) return;

    this.slides = [...document.querySelectorAll('.hero-slide')];
    this.dots   = [...document.querySelectorAll('.hero-dot')];

    if (!this.slides.length) return;

    // Dots
    this.dots.forEach((dot, i) => {
      dot.addEventListener('click', () => this.go(i));
    });

    // Arrows
    document.querySelector('.hero-arrow.prev')?.addEventListener('click', () => this.prev());
    document.querySelector('.hero-arrow.next')?.addEventListener('click', () => this.next());

    // Touch swipe
    let startX = 0;
    this.el.addEventListener('touchstart', e => { startX = e.touches[0].clientX; }, { passive: true });
    this.el.addEventListener('touchend',   e => {
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 50) dx < 0 ? this.next() : this.prev();
    });

    // Keyboard
    document.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft')  this.prev();
      if (e.key === 'ArrowRight') this.next();
    });

    this.go(0);
    this.startAuto();
  },

  go(index) {
    this.slides[this.current]?.classList.remove('active');
    this.dots[this.current]?.classList.remove('active');
    this.current = (index + this.slides.length) % this.slides.length;
    this.slides[this.current]?.classList.add('active');
    this.dots[this.current]?.classList.add('active');
  },

  next() { this.go(this.current + 1); this.restartAuto(); },
  prev() { this.go(this.current - 1); this.restartAuto(); },

  startAuto()   { this.timer = setInterval(() => this.next(), this.interval); },
  stopAuto()    { clearInterval(this.timer); },
  restartAuto() { this.stopAuto(); this.startAuto(); }
};

// ─── BASKET ─────────────────────────────────────────────────────────────────
const Basket = {
  items: JSON.parse(localStorage.getItem('sayohatga_basket') || '[]'),

  save() { localStorage.setItem('sayohatga_basket', JSON.stringify(this.items)); },

  has(id, type) { return this.items.some(i => i.id === id && i.type === type); },

  toggle(id, type, name, img) {
    if (this.has(id, type)) {
      this.items = this.items.filter(i => !(i.id === id && i.type === type));
      this.save();
      this.updateBadge();
      Toast.show(Lang.get('removed_basket'), 'info');
      return false;
    } else {
      this.items.push({ id, type, name, img });
      this.save();
      this.updateBadge();
      Toast.show(Lang.get('success_basket'), 'success');
      return true;
    }
  },

  remove(id, type) {
    this.items = this.items.filter(i => !(i.id === id && i.type === type));
    this.save();
    this.updateBadge();
  },

  updateBadge() {
    const badges = document.querySelectorAll('.basket-badge');
    const count  = this.items.length;
    badges.forEach(b => {
      b.textContent = count;
      b.classList.toggle('show', count > 0);
      if (count > 0) { b.classList.add('bump'); setTimeout(() => b.classList.remove('bump'), 300); }
    });
  },

  syncButtons() {
    document.querySelectorAll('[data-basket-id]').forEach(btn => {
      const id   = btn.dataset.basketId;
      const type = btn.dataset.basketType;
      btn.classList.toggle('in-basket', this.has(id, type));
    });
  },

  init() {
    this.updateBadge();
    this.syncButtons();

    document.addEventListener('click', e => {
      const btn = e.target.closest('[data-basket-id]');
      if (!btn) return;

      const id   = btn.dataset.basketId;
      const type = btn.dataset.basketType;
      const name = btn.dataset.basketName || '';
      const img  = btn.dataset.basketImg  || '';

      fetch('/catalog/basket/toggle/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCsrf(),
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin',
        body: new URLSearchParams({ id, kind: type }).toString()
      })
      .then(r => {
        if (!r.ok) throw new Error('basket_failed');
        return r.json();
      })
      .then(data => {
        if (!data.ok) throw new Error(data.error || 'basket_failed');
        const added = !!data.in_basket;
        btn.classList.toggle('in-basket', added);
        Toast.show(added ? Lang.get('success_basket') : Lang.get('removed_basket'),
                   added ? 'success' : 'info');
        if (data.count !== undefined) {
          document.querySelectorAll('.basket-badge').forEach(b => {
            b.textContent = data.count;
            b.classList.toggle('show', data.count > 0);
            b.classList.add('bump');
            setTimeout(() => b.classList.remove('bump'), 300);
          });
        }
      })
      .catch(() => {
        const added = this.toggle(id, type, name, img);
        btn.classList.toggle('in-basket', added);
      });
    });
  }
};

// ─── LIKES ──────────────────────────────────────────────────────────────────
const Likes = {
  init() {
    document.addEventListener('click', e => {
      const btn = e.target.closest('.like-btn[data-like-id]');
      if (!btn) return;

      const id   = btn.dataset.likeId;
      const type = btn.dataset.likeType; // 'place' or 'accommodation'

      btn.style.pointerEvents = 'none';

      fetch('/catalog/like/toggle/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCsrf(),
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin',
        body: new URLSearchParams({ id, kind: type }).toString()
      })
      .then(r => {
        if (!r.ok) throw new Error('like_failed');
        return r.json();
      })
      .then(data => {
        if (!data.ok) throw new Error(data.error || 'like_failed');
        btn.classList.toggle('active', data.liked);
        const countEl = btn.querySelector('.like-count');
        if (countEl && data.count !== undefined) countEl.textContent = data.count;
        Toast.show(data.liked ? Lang.get('success_like') : '💔', data.liked ? 'success' : 'info');
      })
      .catch(() => {
        btn.classList.toggle('active');
        Toast.show(Lang.get('success_like'), 'success');
      })
      .finally(() => { btn.style.pointerEvents = ''; });
    });
  }
};

// ─── GALLERY ────────────────────────────────────────────────────────────────
const Gallery = {
  init() {
    const main   = document.querySelector('.gallery-main img');
    const thumbs = document.querySelectorAll('.gallery-thumb');
    if (!main || !thumbs.length) return;

    thumbs.forEach((thumb, i) => {
      if (i === 0) thumb.classList.add('active');
      thumb.addEventListener('click', () => {
        main.src = thumb.querySelector('img').src;
        thumbs.forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
      });
    });
  }
};

// ─── SCROLL REVEAL ──────────────────────────────────────────────────────────
const Reveal = {
  init() {
    const els = document.querySelectorAll('.reveal');
    if (!els.length) return;

    const obs = new IntersectionObserver(
      entries => entries.forEach(en => {
        if (en.isIntersecting) { en.target.classList.add('visible'); obs.unobserve(en.target); }
      }),
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );
    els.forEach(el => obs.observe(el));
  }
};

// ─── TOAST NOTIFICATIONS ────────────────────────────────────────────────────
const Toast = {
  container: null,

  init() {
    this.container = document.createElement('div');
    this.container.id = 'toast-container';
    this.container.style.cssText = `
      position:fixed; bottom:24px; right:24px; z-index:9999;
      display:flex; flex-direction:column; gap:10px; pointer-events:none;
    `;
    document.body.appendChild(this.container);
  },

  show(msg, type = 'info', duration = 3000) {
    const t = document.createElement('div');
    const colors = {
      success: { bg: '#d1fae5', color: '#065f46', border: '#059669' },
      error:   { bg: '#fee2e2', color: '#991b1b', border: '#ef4444' },
      info:    { bg: '#dbeafe', color: '#1e40af', border: '#3b82f6' },
      warning: { bg: '#fef3c7', color: '#92400e', border: '#f59e0b' }
    };
    const c = colors[type] || colors.info;

    t.style.cssText = `
      background:${c.bg}; color:${c.color}; border-left:4px solid ${c.border};
      padding:12px 18px; border-radius:10px; font-size:.875rem; font-weight:600;
      box-shadow:0 4px 24px rgba(0,0,0,.12); pointer-events:auto;
      transform:translateX(120%); transition:transform .3s cubic-bezier(.4,0,.2,1);
      max-width:320px; word-break:break-word;
    `;
    t.textContent = msg;
    this.container.appendChild(t);

    requestAnimationFrame(() => {
      requestAnimationFrame(() => { t.style.transform = 'translateX(0)'; });
    });

    setTimeout(() => {
      t.style.transform = 'translateX(120%)';
      setTimeout(() => t.remove(), 320);
    }, duration);
  }
};

// ─── DATE PICKER ─────────────────────────────────────────────────────────────
const DatePicker = {
  init() {
    const today = new Date().toISOString().split('T')[0];
    const fromInput = document.getElementById('id_date_from');
    const toInput   = document.getElementById('id_date_to');

    if (fromInput) {
      fromInput.min = today;
      fromInput.addEventListener('change', () => {
        if (toInput) {
          toInput.min = fromInput.value;
          if (toInput.value && toInput.value <= fromInput.value) toInput.value = '';
        }
      });
    }
    if (toInput) { toInput.min = today; }
  }
};

// ─── GUESTS VALIDATION ───────────────────────────────────────────────────────
const GuestsValidation = {
  init() {
    const guestsInput = document.getElementById('id_guests');
    const maxGuests   = parseInt(document.getElementById('guests-max')?.dataset.max || '99');
    if (!guestsInput) return;

    guestsInput.max = maxGuests;
    guestsInput.addEventListener('input', () => {
      const val = parseInt(guestsInput.value);
      if (val > maxGuests) {
        guestsInput.value = maxGuests;
        Toast.show(`Maksimal ${maxGuests} mehmon`, 'warning');
      }
      if (val < 1) guestsInput.value = 1;
    });
  }
};

// ─── FILTERS ─────────────────────────────────────────────────────────────────
const Filters = {
  init() {
    const regionSel = document.getElementById('filter-region');
    const citySel   = document.getElementById('filter-city');
    if (!regionSel || !citySel) return;

    regionSel.addEventListener('change', () => {
      const regionId = regionSel.value;
      if (!regionId) {
        // Reset cities
        [...citySel.options].forEach((o, i) => { if (i > 0) o.hidden = false; });
        return;
      }
      [...citySel.options].forEach((o, i) => {
        if (i === 0) return;
        o.hidden = o.dataset.region !== regionId;
      });
      citySel.value = '';
    });
  }
};

// ─── COUNTER ANIMATION ───────────────────────────────────────────────────────
const Counter = {
  animateValue(el, start, end, duration) {
    let startTs = null;
    const step = ts => {
      if (!startTs) startTs = ts;
      const progress = Math.min((ts - startTs) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(start + (end - start) * ease).toLocaleString() +
                       (el.dataset.suffix || '');
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  },

  init() {
    const counters = document.querySelectorAll('[data-counter]');
    if (!counters.length) return;

    const obs = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          const el  = en.target;
          const end = parseInt(el.dataset.counter);
          this.animateValue(el, 0, end, 1500);
          obs.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach(c => obs.observe(c));
  }
};

// ─── HELPERS ─────────────────────────────────────────────────────────────────
function getCsrf() {
  return document.cookie.split(';')
    .find(c => c.trim().startsWith('csrftoken='))
    ?.split('=')?.[1] || '';
}

// ─── DJANGO MESSAGES ─────────────────────────────────────────────────────────
function initDjangoMessages() {
  const msgs = document.querySelectorAll('.django-message');
  msgs.forEach(m => {
    const type = m.dataset.type || 'info';
    Toast.show(m.textContent.trim(), type, 5000);
    m.remove();
  });
}

// ─── BOOKING CANCEL CONFIRM ──────────────────────────────────────────────────
function initBookingCancel() {
  document.querySelectorAll('.cancel-booking-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      const form = btn.closest('form');
      if (confirm('Bronni bekor qilmoqchimisiz?')) form?.submit();
    });
  });
}

// ─── INIT ────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  Toast.init();
  Theme.init();
  Lang.init();
  Header.init();
  Carousel.init();
  Basket.init();
  Likes.init();
  Gallery.init();
  Reveal.init();
  DatePicker.init();
  GuestsValidation.init();
  Filters.init();
  Counter.init();
  initDjangoMessages();
  initBookingCancel();
});

// Export for template use
window.Sayohatga = { Lang, Theme, Basket, Toast };
