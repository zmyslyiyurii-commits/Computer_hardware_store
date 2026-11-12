from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import F


class Category(models.Model):
    # Категорія об'єднує товари одного типу, наприклад ноутбуки чи монітори.
    name = models.CharField('Назва', max_length=100, unique=True)
    icon = models.CharField('Іконка', max_length=8, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'категорія'
        verbose_name_plural = 'категорії'

    def __str__(self):
        return self.name


class Product(models.Model):
    COMPONENT_TYPE_CHOICES = (
        ('processor', 'Процесори'),
        ('motherboard', 'Материнські плати'),
        ('graphics_card', 'Відеокарти'),
        ('memory', "Оперативна пам’ять"),
        ('ssd', 'SSD накопичувачі'),
        ('hdd', 'Жорсткі диски HDD'),
        ('case', 'Корпуси'),
        ('power_supply', 'Блоки живлення'),
        ('cooling', 'Системи охолодження'),
    )
    NETWORK_PRODUCT_TYPE_CHOICES = (
        ('мережевий розгалужувач', 'Мережевий розгалужувач'),
        ('мережеві подовжувачі', 'Мережеві подовжувачі'),
        ('мережеві фільтри живлення', 'Мережеві фільтри живлення'),
    )
    PERIPHERAL_TYPE_CHOICES = (
        ('keyboard', 'Клавіатури'),
        ('mouse', 'Мишки'),
        ('mouse_pad', 'Килимки'),
    )

    # Основні дані товару, які редагуються через адміністративну панель.
    name = models.CharField('Назва', max_length=200)
    category = models.ForeignKey(
        Category,
        # Не дозволяємо видалити категорію, поки до неї прив'язані товари.
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категорія',
    )
    price = models.DecimalField(
        'Ціна',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    stock_quantity = models.PositiveIntegerField('Кількість на складі', default=0)
    image_url = models.URLField('Посилання на фото', blank=True)
    component_type = models.CharField(
        'Тип комплектуючого для ПК',
        max_length=30,
        choices=COMPONENT_TYPE_CHOICES,
        blank=True,
    )
    peripheral_type = models.CharField(
        'Тип периферії',
        max_length=20,
        choices=PERIPHERAL_TYPE_CHOICES,
        blank=True,
    )
    badge = models.CharField('Бейдж', max_length=50, blank=True)
    is_featured = models.BooleanField(
        'Показувати в «Популярне зараз»',
        default=False,
        help_text='Познач товар, якщо він має відображатися в блоці на головній сторінці.',
    )
    description = models.TextField('Опис', blank=True)
    manufacturer = models.CharField('Виробник', max_length=100, blank=True)
    model_series = models.CharField('Серія (модельний ряд)', max_length=100, blank=True)
    laptop_type = models.CharField('Тип ноутбуку', max_length=60, blank=True)
    display_diagonal = models.CharField('Діагональ дисплея', max_length=30, blank=True)
    resolution = models.CharField('Роздільна здатність', max_length=30, blank=True)
    matrix_type = models.CharField('Тип матриці', max_length=30, blank=True)
    screen_surface = models.CharField('Поверхня екрану', max_length=40, blank=True)
    refresh_rate = models.CharField('Частота оновлення екрану', max_length=20, blank=True)
    intel_generation = models.CharField('Покоління процесора Intel', max_length=30, blank=True)
    amd_generation = models.CharField('Покоління процесора AMD', max_length=30, blank=True)
    processor = models.CharField('Процесор', max_length=100, blank=True)
    processor_cores = models.CharField('Кількість ядер процесора', max_length=10, blank=True)
    ram_type = models.CharField("Тип оперативної пам'яті", max_length=20, blank=True)
    ram_capacity = models.CharField("Об'єм оперативної пам'яті", max_length=20, blank=True)
    ram_slots = models.CharField('Кількість слотів для оперативної пам’яті', max_length=50, blank=True)
    ssd_capacity = models.CharField('Об’єм SSD', max_length=30, blank=True)
    graphics_type = models.CharField('Тип відеокарти', max_length=30, blank=True)
    discrete_graphics_series = models.CharField('Серія дискретної відеокарти', max_length=100, blank=True)
    video_memory = models.CharField('Об’єм відеопам’яті', max_length=30, blank=True)
    wireless_technologies = models.TextField(
        'Бездротові технології',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    interfaces = models.TextField(
        'Інтерфейси та підключення',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    operating_system = models.CharField('Операційна система', max_length=100, blank=True)
    battery_capacity = models.CharField('Ємність акумулятора', max_length=40, blank=True)
    webcam = models.CharField('Веб-камера', max_length=100, blank=True)
    additional_features = models.TextField('Додаткові можливості', blank=True)
    width = models.CharField('Ширина, мм', max_length=30, blank=True)
    height = models.CharField('Висота, мм', max_length=30, blank=True)
    depth = models.CharField('Глибина, мм', max_length=30, blank=True)
    country_of_origin = models.CharField('Країна виробництва', max_length=100, blank=True)
    warranty_months = models.PositiveSmallIntegerField('Гарантія, міс.', blank=True, null=True)
    features = models.TextField(
        'Особливості',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    weight = models.CharField('Вага', max_length=30, blank=True)
    color = models.CharField('Колір', max_length=30, blank=True)
    computer_type = models.CharField('Тип ПК', max_length=60, blank=True)
    computer_view = models.CharField('Вид комп’ютера', max_length=60, blank=True)
    processor_threads = models.CharField('Кількість потоків', max_length=20, blank=True)
    processor_frequency = models.CharField('Частота процесора, ГГц', max_length=30, blank=True)
    processor_boost_frequency = models.CharField('Частота в Boost, ГГц', max_length=30, blank=True)
    processor_boost_supported = models.CharField('Підтримка Boost режиму', max_length=30, blank=True)
    motherboard_socket = models.CharField('Сокет', max_length=40, blank=True)
    motherboard_chipset = models.CharField('Чипсет', max_length=100, blank=True)
    graphics_card_manufacturer = models.CharField('Виробник чипу відеокарти', max_length=100, blank=True)
    ram_form_factor = models.CharField('Форм-фактор пам’яті', max_length=40, blank=True)
    ram_frequency = models.CharField('Частота пам’яті', max_length=40, blank=True)
    ram_standard = models.CharField('Стандарт пам’яті', max_length=40, blank=True)
    ram_max_capacity = models.CharField('Максимальний об’єм пам’яті', max_length=40, blank=True)
    storage_types = models.CharField('Типи внутрішніх накопичувачів', max_length=100, blank=True)
    hdd_capacity = models.CharField('Об’єм HDD', max_length=40, blank=True)
    optical_drive = models.CharField('Оптичний привід', max_length=60, blank=True)
    card_reader = models.CharField('Кардридер', max_length=60, blank=True)
    built_in_microphone = models.CharField('Вбудований мікрофон', max_length=60, blank=True)
    built_in_speakers = models.CharField('Вбудовані динаміки', max_length=60, blank=True)
    audio_controller = models.CharField('Аудіоконтролер', max_length=150, blank=True)
    multichannel_audio = models.CharField('Багатоканальний звук', max_length=40, blank=True)
    wired_network = models.CharField('Провідна мережа (LAN)', max_length=80, blank=True)
    peripherals_included = models.CharField('Пристрої введення в комплекті', max_length=150, blank=True)
    case_model = models.CharField('Модель корпусу', max_length=100, blank=True)
    case_metal_thickness = models.CharField('Товщина металу корпусу', max_length=40, blank=True)
    case_material = models.CharField('Матеріал корпусу', max_length=100, blank=True)
    psu_location = models.CharField('Розташування блоку живлення', max_length=60, blank=True)
    psu_power = models.CharField('Потужність блоку живлення', max_length=40, blank=True)
    case_lighting = models.CharField('Підсвічування корпусу', max_length=150, blank=True)
    cooling = models.TextField('Охолодження', blank=True)
    computer_manufacturer = models.CharField('Виробник', max_length=100, blank=True)
    computer_display_diagonal = models.CharField('Діагональ екрану', max_length=30, blank=True)
    computer_screen_type = models.CharField('Тип екрану', max_length=50, blank=True)
    computer_processor_series = models.CharField('Серія процесора', max_length=100, blank=True)
    computer_intel_generation = models.CharField('Покоління процесора Intel', max_length=30, blank=True)
    computer_amd_generation = models.CharField('Покоління процесора AMD', max_length=30, blank=True)
    computer_processor = models.CharField('Модель процесора', max_length=100, blank=True)
    computer_processor_cores = models.CharField('Кількість ядер процесора', max_length=10, blank=True)
    computer_ram_type = models.CharField("Тип оперативної пам'яті", max_length=20, blank=True)
    computer_ram_capacity = models.CharField("Об'єм оперативної пам'яті", max_length=20, blank=True)
    computer_ram_slots = models.CharField('Кількість слотів пам’яті', max_length=50, blank=True)
    computer_ram_frequency = models.CharField('Частота пам’яті', max_length=40, blank=True)
    computer_ram_standard = models.CharField('Стандарт пам’яті', max_length=40, blank=True)
    computer_ram_max_capacity = models.CharField('Максимальний об’єм пам’яті', max_length=40, blank=True)
    computer_ssd_capacity = models.CharField('Об’єм SSD', max_length=30, blank=True)
    computer_graphics_type = models.CharField('Тип відеокарти', max_length=30, blank=True)
    computer_discrete_graphics_series = models.CharField('Модель відеокарти', max_length=100, blank=True)
    computer_video_memory = models.CharField('Об’єм відеопам’яті', max_length=30, blank=True)
    computer_wireless_technologies = models.TextField(
        'Бездротові технології',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    computer_interfaces = models.TextField(
        'Зовнішні порти та роз’єми',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    computer_operating_system = models.CharField('Операційна система', max_length=100, blank=True)
    computer_webcam = models.CharField('Вбудована веб-камера', max_length=100, blank=True)
    computer_additional_features = models.TextField('Додаткові можливості', blank=True)
    computer_vesa_support = models.CharField('Можливість кріплення VESA', max_length=40, blank=True)
    computer_vr_support = models.CharField('Підтримка VR', max_length=40, blank=True)
    computer_backlit = models.CharField('Підсвічування', max_length=40, blank=True)
    computer_width = models.CharField('Ширина корпусу, мм', max_length=30, blank=True)
    computer_height = models.CharField('Висота корпусу, мм', max_length=30, blank=True)
    computer_depth = models.CharField('Глибина корпусу, мм', max_length=30, blank=True)
    computer_country_of_origin = models.CharField('Країна виробництва', max_length=100, blank=True)
    computer_warranty_months = models.PositiveSmallIntegerField('Гарантія, міс.', blank=True, null=True)
    computer_features = models.TextField('Примітка', blank=True)
    computer_weight = models.CharField('Вага', max_length=30, blank=True)
    computer_color = models.CharField('Колір корпусу', max_length=30, blank=True)
    computer_processor_frequency = models.CharField('Частота процесора, ГГц', max_length=30, blank=True)
    computer_storage_types = models.CharField('Типи внутрішніх накопичувачів', max_length=100, blank=True)
    computer_hdd_capacity = models.CharField('Об’єм HDD', max_length=40, blank=True)
    computer_optical_drive = models.CharField('Оптичний привід', max_length=60, blank=True)
    computer_card_reader = models.CharField('Кардридер', max_length=60, blank=True)
    computer_built_in_microphone = models.CharField('Вбудований мікрофон', max_length=60, blank=True)
    computer_built_in_speakers = models.CharField('Вбудовані динаміки', max_length=60, blank=True)
    computer_audio_controller = models.CharField('Аудіоконтролер', max_length=150, blank=True)
    computer_multichannel_audio = models.CharField('Багатоканальний звук', max_length=40, blank=True)
    computer_wired_network = models.CharField('Провідна мережа (LAN)', max_length=80, blank=True)
    computer_peripherals_included = models.CharField('Пристрої введення в комплекті', max_length=150, blank=True)
    cpu_manufacturer = models.CharField('Виробник процесора', max_length=30, blank=True)
    cpu_family = models.CharField('Сімейство процесора', max_length=100, blank=True)
    cpu_socket = models.CharField('Сокет процесора', max_length=30, blank=True)
    cpu_core_count = models.CharField('Кількість ядер процесора', max_length=30, blank=True)
    cpu_thread_count = models.CharField('Кількість потоків процесора', max_length=30, blank=True)
    cpu_base_clock = models.CharField('Базова тактова частота процесора', max_length=30, blank=True)
    cpu_max_clock = models.CharField('Максимальна тактова частота процесора', max_length=30, blank=True)
    cpu_tdp = models.CharField('Максимальний TDP процесора', max_length=30, blank=True)
    cpu_process_technology = models.CharField('Техпроцес', max_length=30, blank=True)
    cpu_l1_cache = models.CharField('Об’єм кеш-пам’яті 1-го рівня', max_length=30, blank=True)
    cpu_l2_cache = models.CharField('Об’єм кеш-пам’яті 2-го рівня', max_length=30, blank=True)
    cpu_l3_cache = models.CharField('Об’єм кеш-пам’яті 3-го рівня', max_length=30, blank=True)
    cpu_max_memory = models.CharField('Максимальний обсяг оперативної пам’яті', max_length=30, blank=True)
    cpu_memory_type = models.CharField('Тип оперативної пам’яті', max_length=30, blank=True)
    cpu_max_memory_speed = models.CharField('Максимальна швидкість пам’яті', max_length=30, blank=True)
    cpu_memory_channels = models.CharField('Кількість каналів пам’яті', max_length=20, blank=True)
    cpu_integrated_graphics = models.CharField('Графічне ядро процесора', max_length=100, blank=True)
    cpu_intel_generation = models.CharField('Покоління процесорів Intel', max_length=100, blank=True)
    cpu_amd_architecture = models.CharField('Архітектура ядра AMD', max_length=50, blank=True)
    cpu_max_temperature = models.CharField('Максимально допустима температура', max_length=30, blank=True)
    cpu_unlocked_multiplier = models.CharField('Розблокований множник', max_length=20, blank=True)
    cpu_pcie_version = models.CharField('Версія PCI Express', max_length=20, blank=True)
    cpu_release_date = models.DateField('Дата виходу', blank=True, null=True)
    cpu_package_type = models.CharField('Тип поставки процесора', max_length=40, blank=True)
    cpu_cooling_included = models.CharField('Охолодження в комплекті', max_length=40, blank=True)
    cpu_country_of_origin = models.CharField('Країна виробництва', max_length=100, blank=True)
    cpu_warranty_months = models.PositiveSmallIntegerField('Гарантія, міс.', blank=True, null=True)
    cpu_barcode = models.CharField('Штрихкод', max_length=80, blank=True)
    cpu_note = models.TextField('Примітка до процесора', blank=True)
    motherboard_manufacturer = models.CharField('Виробник материнської плати', max_length=100, blank=True)
    motherboard_available_today = models.BooleanField('Можна отримати сьогодні', default=False)
    motherboard_purpose = models.CharField('Призначення материнської плати', max_length=50, blank=True)
    motherboard_product_socket = models.CharField('Сокет материнської плати', max_length=40, blank=True)
    motherboard_pcie_x1_slots = models.CharField('PCI Express x1', max_length=30, blank=True)
    motherboard_pcie_x4_slots = models.CharField('PCI Express x4', max_length=30, blank=True)
    motherboard_pcie_x16_slots = models.CharField('PCI Express x16', max_length=30, blank=True)
    motherboard_pci_slots = models.CharField('Слоти PCI', max_length=30, blank=True)
    motherboard_chipset_model = models.CharField('Модель чипсета', max_length=100, blank=True)
    motherboard_ram_type = models.CharField('Тип оперативної пам’яті материнської плати', max_length=40, blank=True)
    motherboard_ram_slots = models.CharField('Кількість роз’ємів оперативної пам’яті', max_length=30, blank=True)
    motherboard_max_ram = models.CharField('Максимальний об’єм оперативної пам’яті', max_length=30, blank=True)
    motherboard_max_ram_frequency = models.CharField('Максимальна частота оперативної пам’яті', max_length=30, blank=True)
    motherboard_integrated_video = models.CharField('Вбудоване відео', max_length=80, blank=True)
    motherboard_lan_speed = models.CharField('Швидкість LAN портів', max_length=30, blank=True)
    motherboard_video_outputs = models.TextField('Відеовиходи', blank=True, help_text='Якщо значень кілька, розділяйте їх комами.')
    motherboard_usb = models.TextField('USB', blank=True, help_text='Якщо значень кілька, розділяйте їх комами.')
    motherboard_digital_audio_output = models.CharField('Цифровий аудіо роз’єм (S/PDIF)', max_length=100, blank=True)
    motherboard_m2_slots = models.CharField('Кількість роз’ємів M.2', max_length=30, blank=True)
    motherboard_sata3_ports = models.CharField('Кількість SATA-III портів', max_length=30, blank=True)
    motherboard_satae_slot = models.CharField('SATAe роз’єм', max_length=50, blank=True)
    motherboard_u2_slot = models.CharField('U.2 роз’єм', max_length=50, blank=True)
    motherboard_wireless = models.TextField('Бездротовий зв’язок материнської плати', blank=True, help_text='Якщо значень кілька, розділяйте їх комами.')
    motherboard_raid_controller = models.CharField('Контролер RAID', max_length=50, blank=True)
    motherboard_search_tag = models.CharField('Також шукають', max_length=100, blank=True)
    motherboard_form_factor = models.CharField('Форм-фактор материнської плати', max_length=50, blank=True)
    motherboard_supported_processors = models.TextField('Підтримка процесорів', blank=True)
    motherboard_expansion_slots = models.TextField('Слоти розширення', blank=True)
    motherboard_ram_frequencies = models.TextField('Частота оперативної пам’яті', blank=True)
    motherboard_dual_channel_support = models.CharField('Підтримка двоканального режиму', max_length=20, blank=True)
    motherboard_ecc_support = models.CharField('Підтримка ECC', max_length=20, blank=True)
    motherboard_audio_controller = models.CharField('Аудіоконтролер', max_length=100, blank=True)
    motherboard_multichannel_audio = models.CharField('Багатоканальний звук', max_length=30, blank=True)
    motherboard_lan_port_count = models.CharField('Кількість LAN портів', max_length=30, blank=True)
    motherboard_network_adapter = models.CharField('Тип мережевої карти', max_length=100, blank=True)
    motherboard_rear_ports = models.TextField('Зовнішні порти', blank=True)
    motherboard_internal_ports = models.TextField('Внутрішні роз’єми і порти', blank=True)
    motherboard_power_connector = models.CharField('Конектор живлення', max_length=100, blank=True)
    motherboard_headers = models.TextField('Колодки', blank=True)
    motherboard_fan_headers = models.CharField('4-pin для вентилятора', max_length=50, blank=True)
    motherboard_other_connectors = models.TextField('Інші коннектори', blank=True)
    motherboard_bios_type = models.CharField('Тип BIOS', max_length=150, blank=True)
    motherboard_operating_system = models.CharField('Підтримка ОС', max_length=100, blank=True)
    motherboard_height = models.CharField('Висота, мм', max_length=30, blank=True)
    motherboard_width = models.CharField('Ширина, мм', max_length=30, blank=True)
    motherboard_country_of_origin = models.CharField('Країна виробництва', max_length=100, blank=True)
    motherboard_warranty_months = models.PositiveSmallIntegerField('Гарантія, міс.', blank=True, null=True)
    motherboard_barcode = models.CharField('Штрихкод', max_length=80, blank=True)
    motherboard_note = models.TextField('Примітка', blank=True)
    video_card_manufacturer = models.CharField('Виробник', max_length=100, blank=True)
    video_card_family = models.CharField('Сімейство графіки', max_length=50, blank=True)
    video_card_form_factor = models.CharField('Форм-фактор відеокарти', max_length=50, blank=True)
    video_card_purpose = models.CharField('Призначення відеокарти', max_length=50, blank=True)
    video_card_chip = models.CharField('Графічний чип', max_length=100, blank=True)
    video_card_interface = models.CharField('Інтерфейс відеокарти', max_length=50, blank=True)
    video_card_memory_capacity = models.CharField('Об’єм вбудованої пам’яті', max_length=30, blank=True)
    video_card_memory_type = models.CharField('Тип пам’яті відеокарти', max_length=30, blank=True)
    video_card_memory_bus = models.CharField('Розрядність шини пам’яті', max_length=30, blank=True)
    video_card_connectors = models.TextField('Роз’єми відеокарти', blank=True)
    video_card_cooling_system = models.CharField('Тип системи охолодження', max_length=50, blank=True)
    video_card_cooling_type = models.CharField('Вид охолодження відеокарти', max_length=50, blank=True)
    video_card_fan_count = models.CharField('Кількість вентиляторів відеокарти', max_length=30, blank=True)
    video_card_power_connectors = models.CharField('Роз’єми додаткового живлення відеокарти', max_length=50, blank=True)
    video_card_boost_clock = models.CharField('Частота ядра (Boost)', max_length=30, blank=True)
    video_card_memory_frequency = models.CharField('Частота пам’яті', max_length=30, blank=True)
    video_card_max_displays = models.CharField('Максимальне число дисплеїв', max_length=20, blank=True)
    video_card_max_resolution = models.CharField('Максимальна роздільна здатність', max_length=50, blank=True)
    video_card_hdcp = models.CharField('Сумісність з HDCP', max_length=20, blank=True)
    video_card_recommended_psu = models.CharField(
        'Мінімальна рекомендована потужність блоку живлення',
        max_length=30,
        blank=True,
    )
    video_card_directx = models.CharField('Версія DirectX', max_length=30, blank=True)
    video_card_opengl = models.CharField('Версія OpenGL', max_length=30, blank=True)
    video_card_dlss = models.CharField('Версія DLSS', max_length=50, blank=True)
    video_card_dimensions = models.CharField('Розміри', max_length=50, blank=True)
    video_card_weight = models.CharField('Вага', max_length=30, blank=True)
    video_card_country_of_origin = models.CharField('Країна виробництва', max_length=100, blank=True)
    video_card_warranty_months = models.PositiveSmallIntegerField('Гарантія, міс.', blank=True, null=True)
    video_card_barcode = models.CharField('Штрихкод', max_length=80, blank=True)
    video_card_note = models.TextField('Примітка', blank=True)
    memory_purpose = models.CharField('Призначення оперативної пам’яті', max_length=40, blank=True)
    memory_manufacturer = models.CharField('Виробник', max_length=100, blank=True)
    memory_type = models.CharField('Тип пам’яті', max_length=20, blank=True)
    memory_capacity = models.CharField('Об’єм пам’яті', max_length=20, blank=True)
    memory_frequency = models.CharField('Частота пам’яті', max_length=20, blank=True)
    memory_module_count = models.CharField('Кількість модулів у наборі', max_length=20, blank=True)
    memory_timing = models.CharField('Таймінги', max_length=20, blank=True)
    memory_voltage = models.CharField('Напруга живлення', max_length=20, blank=True)
    memory_cooling = models.CharField('Охолодження', max_length=30, blank=True)
    memory_lighting = models.CharField('Підсвічування', max_length=20, blank=True)
    memory_overclock_profiles = models.CharField(
        'Розширені профілі розгону',
        max_length=50,
        blank=True,
        help_text='Якщо профілів кілька, розділяйте їх комами.',
    )
    memory_standard = models.CharField('Стандарти пам’яті', max_length=40, blank=True)
    memory_form_factor = models.CharField('Форм-фактор пам’яті', max_length=40, blank=True)
    memory_ecc = models.CharField('Перевірка і корекція помилок (ECC)', max_length=20, blank=True)
    memory_buffering = models.CharField('Буферизація', max_length=30, blank=True)
    memory_additional_note = models.TextField('Додаткова примітка', blank=True)
    memory_country_of_origin = models.CharField('Країна виробництва', max_length=100, blank=True)
    memory_warranty_months = models.PositiveSmallIntegerField('Гарантія, міс.', blank=True, null=True)
    memory_barcode = models.CharField('Штрихкод', max_length=80, blank=True)
    memory_note = models.TextField('Примітка', blank=True)
    ssd_manufacturer = models.CharField('Виробник SSD', max_length=100, blank=True)
    ssd_drive_type = models.CharField('Тип накопичувача', max_length=30, blank=True)
    ssd_component_capacity = models.CharField('Об’єм SSD накопичувача', max_length=30, blank=True)
    ssd_flash_type = models.CharField('Тип флеш-пам’яті', max_length=40, blank=True)
    ssd_form_factor = models.CharField('Форм-фактор SSD', max_length=30, blank=True)
    ssd_m2_size = models.CharField('Типорозмір M.2', max_length=30, blank=True)
    ssd_interface = models.CharField('Інтерфейс підключення SSD', max_length=50, blank=True)
    ssd_read_speed = models.CharField('Швидкість читання SSD', max_length=40, blank=True)
    ssd_write_speed = models.CharField('Швидкість запису SSD', max_length=40, blank=True)
    ssd_thickness = models.CharField('Товщина SSD', max_length=30, blank=True)
    ssd_endurance = models.CharField('Напрацювання на відмову SSD', max_length=40, blank=True)
    ssd_tbw = models.CharField('TBW SSD', max_length=30, blank=True)
    ssd_power_consumption = models.CharField('Енергоспоживання SSD', max_length=30, blank=True)
    ssd_dimensions = models.CharField('Габарити SSD', max_length=100, blank=True)
    ssd_weight = models.CharField('Вага SSD', max_length=30, blank=True)
    ssd_color = models.CharField('Колір SSD', max_length=30, blank=True)
    ssd_country_of_origin = models.CharField('Країна виробництва SSD', max_length=100, blank=True)
    ssd_warranty_months = models.PositiveSmallIntegerField('Гарантія SSD, міс.', blank=True, null=True)
    ssd_barcode = models.CharField('Штрихкод SSD', max_length=80, blank=True)
    ssd_note = models.TextField('Примітка до SSD', blank=True)
    hdd_drive_type = models.CharField('Тип HDD', max_length=40, blank=True)
    hdd_manufacturer = models.CharField('Виробник HDD', max_length=100, blank=True)
    hdd_component_capacity = models.CharField('Об’єм HDD накопичувача', max_length=30, blank=True)
    hdd_form_factor = models.CharField('Форм-фактор HDD', max_length=20, blank=True)
    hdd_rpm = models.CharField('Швидкість обертання HDD', max_length=30, blank=True)
    hdd_buffer_size = models.CharField('Розмір буфера HDD', max_length=30, blank=True)
    hdd_interface = models.CharField('Інтерфейс HDD', max_length=40, blank=True)
    hdd_series = models.CharField('Лінійка (серія) HDD', max_length=100, blank=True)
    hdd_country_of_origin = models.CharField('Країна виробництва HDD', max_length=100, blank=True)
    hdd_warranty_months = models.PositiveSmallIntegerField('Гарантія HDD, міс.', blank=True, null=True)
    hdd_barcode = models.CharField('Штрихкод HDD', max_length=80, blank=True)
    hdd_note = models.TextField('Примітка до HDD', blank=True)
    case_manufacturer = models.CharField('Виробник корпусу', max_length=100, blank=True)
    case_class = models.CharField('Клас корпусу', max_length=40, blank=True)
    case_form_factor = models.CharField('Типорозмір корпусу', max_length=40, blank=True)
    case_installation = models.CharField('Спосіб встановлення корпусу', max_length=40, blank=True)
    case_supported_motherboards = models.TextField(
        'Підтримувані материнські плати',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    case_psu_included = models.CharField('Наявність блоку живлення', max_length=40, blank=True)
    case_3_5_bays = models.CharField('Кількість внутрішніх відсіків 3.5"', max_length=20, blank=True)
    case_fan_configuration = models.TextField(
        'Кількість і розмір вентиляторів',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    case_external_connectors = models.TextField(
        'Зовнішні роз’єми корпусу',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    case_color = models.CharField('Колір корпусу', max_length=40, blank=True)
    case_external_bays_5_25 = models.CharField('Кількість зовнішніх відсіків 5.25"', max_length=30, blank=True)
    case_external_bays_3_5 = models.CharField('Кількість зовнішніх відсіків 3.5"', max_length=30, blank=True)
    case_internal_bays_5_25 = models.CharField('Кількість внутрішніх відсіків 5.25"', max_length=30, blank=True)
    case_internal_bays_2_5 = models.CharField('Кількість внутрішніх відсіків 2.5"', max_length=30, blank=True)
    case_expansion_slots = models.CharField('Кількість слотів розширення', max_length=30, blank=True)
    case_additional_fan_positions = models.TextField('Місця для додаткових вентиляторів', blank=True)
    case_cooling_elements = models.TextField('Охолоджуючі елементи корпусу', blank=True)
    case_dust_filter = models.CharField('Пиловий фільтр корпусу', max_length=30, blank=True)
    case_liquid_cooling_support = models.CharField('Підтримка рідинного охолодження', max_length=30, blank=True)
    case_max_noise = models.CharField('Максимальний рівень шуму корпусу', max_length=30, blank=True)
    case_gpu_clearance = models.CharField('Встановлення довгих відеокарт', max_length=30, blank=True)
    case_cpu_cooler_clearance = models.CharField('Максимальна висота процесорного кулера', max_length=30, blank=True)
    case_dimensions = models.CharField('Розмір корпусу, мм', max_length=60, blank=True)
    case_weight = models.CharField('Вага корпусу, кг', max_length=30, blank=True)
    case_country_of_origin = models.CharField('Країна виробництва корпусу', max_length=100, blank=True)
    case_warranty_months = models.PositiveSmallIntegerField('Гарантія корпусу, міс.', blank=True, null=True)
    case_barcode = models.CharField('Штрихкод корпусу', max_length=80, blank=True)
    case_note = models.TextField('Примітка до корпусу', blank=True)
    psu_manufacturer = models.CharField('Виробник блоку живлення', max_length=100, blank=True)
    psu_type = models.CharField('Тип блоку живлення', max_length=60, blank=True)
    psu_standard = models.CharField('Стандарт блоку живлення', max_length=40, blank=True)
    psu_wattage = models.CharField('Потужність блоку живлення, Вт', max_length=30, blank=True)
    psu_modular_connection = models.CharField('Модульне підключення кабелів', max_length=30, blank=True)
    psu_certification = models.CharField('Сертифікація 80 PLUS', max_length=40, blank=True)
    psu_pfc = models.CharField('Модуль PFC', max_length=30, blank=True)
    psu_pcie_connectors = models.CharField('Кількість роз’ємів додаткового живлення для відеокарт', max_length=30, blank=True)
    psu_sata_connectors = models.CharField('Кількість роз’ємів SATA', max_length=30, blank=True)
    psu_fan_diameter = models.CharField('Діаметр вентилятора блоку живлення', max_length=30, blank=True)
    psu_motherboard_connector = models.CharField('Підключення материнської плати', max_length=60, blank=True)
    psu_cpu_connector = models.CharField('Підключення процесора', max_length=60, blank=True)
    psu_gpu_connector = models.CharField('Підключення відеокарти', max_length=80, blank=True)
    psu_peripheral_connectors = models.CharField('Кількість роз’ємів Peripheral', max_length=30, blank=True)
    psu_output_current_5v = models.CharField('Output Current +5V', max_length=20, blank=True)
    psu_output_current_3_3v = models.CharField('Output Current +3.3V', max_length=20, blank=True)
    psu_output_current_12v = models.CharField('Output Current +12V', max_length=20, blank=True)
    psu_output_current_minus_12v = models.CharField('Output Current -12V', max_length=20, blank=True)
    psu_output_current_5vsb = models.CharField('Output Current +5Vsb', max_length=20, blank=True)
    psu_cooling_type = models.CharField('Тип охолодження блоку живлення', max_length=40, blank=True)
    psu_protection = models.TextField('Захист блоку живлення', blank=True)
    psu_dimensions = models.CharField('Розмір блоку живлення, мм', max_length=80, blank=True)
    psu_country_of_origin = models.CharField('Країна виробництва блоку живлення', max_length=100, blank=True)
    psu_warranty_months = models.PositiveSmallIntegerField('Гарантія блоку живлення, міс.', blank=True, null=True)
    psu_barcode = models.CharField('Штрихкод блоку живлення', max_length=80, blank=True)
    cooling_manufacturer = models.CharField('Виробник системи охолодження', max_length=100, blank=True)
    cooling_cpu_compatibility = models.TextField(
        'Сумісність із процесорами',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    cooling_socket = models.TextField(
        'Сокет',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    cooling_fan_count = models.CharField('Кількість вентиляторів системи охолодження', max_length=30, blank=True)
    cooling_fan_diameter = models.CharField('Діаметр вентиляторів системи охолодження', max_length=40, blank=True)
    cooling_lighting = models.CharField('Підсвічування системи охолодження', max_length=30, blank=True)
    cooling_max_tdp = models.CharField('Максимальний TDP системи охолодження', max_length=30, blank=True)
    cooling_max_fan_speed = models.CharField('Максимальна частота обертів вентиляторів системи охолодження', max_length=30, blank=True)
    cooling_radiator_material = models.CharField('Матеріал радіатора системи охолодження', max_length=60, blank=True)
    cooling_airflow = models.CharField('Повітряний потік системи охолодження', max_length=30, blank=True)
    cooling_fan_speed_control = models.CharField('Управління швидкістю обертання вентиляторів', max_length=30, blank=True)
    cooling_pump_power_connector = models.CharField('Роз’єм живлення помпи', max_length=40, blank=True)
    cooling_fan_power_connector = models.CharField('Роз’єм живлення вентиляторів', max_length=40, blank=True)
    cooling_pump_voltage = models.CharField('Напруга живлення помпи', max_length=20, blank=True)
    cooling_tube_length = models.CharField('Довжина патрубків системи охолодження', max_length=30, blank=True)
    cooling_radiator_dimensions = models.CharField('Розміри радіатора системи охолодження', max_length=60, blank=True)
    cooling_fan_dimensions = models.CharField('Розміри вентиляторів системи охолодження', max_length=60, blank=True)
    cooling_pump_dimensions = models.CharField('Розмір водоблоку системи охолодження', max_length=60, blank=True)
    cooling_noise_level = models.CharField('Рівень шуму системи охолодження', max_length=30, blank=True)
    cooling_color = models.CharField('Колір системи охолодження', max_length=40, blank=True)
    cooling_country_of_origin = models.CharField('Країна виробництва системи охолодження', max_length=100, blank=True)
    cooling_warranty_months = models.PositiveSmallIntegerField('Гарантія системи охолодження, міс.', blank=True, null=True)
    cooling_barcode = models.CharField('Штрихкод системи охолодження', max_length=80, blank=True)
    cooling_note = models.TextField('Примітка до системи охолодження', blank=True)
    monitor_aspect_ratio = models.CharField('Співвідношення сторін монітора', max_length=20, blank=True)
    monitor_backlight = models.CharField('Підсвічування монітора', max_length=40, blank=True)
    monitor_response_time = models.CharField('Час реакції матриці монітора', max_length=30, blank=True)
    monitor_stand_adjustment = models.TextField(
        'Регулювання положення монітора',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    monitor_vesa = models.CharField('Кріплення VESA монітора', max_length=40, blank=True)
    monitor_display_type = models.CharField('Тип монітора', max_length=100, blank=True)
    monitor_brightness = models.CharField('Яскравість монітора', max_length=30, blank=True)
    monitor_static_contrast = models.CharField('Статична контрастність монітора', max_length=30, blank=True)
    monitor_dynamic_contrast = models.CharField('Динамічна контрастність монітора', max_length=30, blank=True)
    monitor_viewing_angles = models.CharField('Кути огляду монітора', max_length=30, blank=True)
    monitor_max_colors = models.CharField('Максимальна кількість кольорів монітора', max_length=30, blank=True)
    monitor_image_enhancement = models.TextField('Технології покращення зображення монітора', blank=True)
    monitor_sync_technology = models.CharField('Технології синхронізації монітора', max_length=100, blank=True)
    monitor_tilt_angle = models.CharField('Регулювання нахилу монітора', max_length=50, blank=True)
    monitor_power_consumption = models.CharField('Споживана потужність монітора в робочому режимі', max_length=30, blank=True)
    monitor_standby_power = models.CharField('Споживана потужність монітора в режимі очікування', max_length=30, blank=True)
    monitor_dimensions_with_stand = models.CharField('Розміри монітора з підставкою', max_length=60, blank=True)
    monitor_dimensions_without_stand = models.CharField('Розміри монітора без підставки', max_length=60, blank=True)
    monitor_weight_unboxed = models.CharField('Вага монітора без упаковки', max_length=30, blank=True)
    monitor_weight_boxed = models.CharField('Вага монітора з упаковкою', max_length=30, blank=True)
    network_product_type = models.CharField(
        'Тип мережевого обладнання',
        max_length=80,
        choices=NETWORK_PRODUCT_TYPE_CHOICES,
        blank=True,
    )
    network_socket_count = models.CharField('Кількість розеток мережевого обладнання', max_length=20, blank=True)
    network_outlet_type = models.CharField('Тип вихідних розеток мережевого обладнання', max_length=100, blank=True)
    network_input_plug_type = models.CharField('Тип вхідної вилки мережевого обладнання', max_length=100, blank=True)
    network_usb_ports = models.CharField('USB-порти мережевого обладнання', max_length=40, blank=True)
    network_cable_length = models.CharField('Довжина кабелю мережевого обладнання', max_length=30, blank=True)
    network_cable_specification = models.CharField(
        'Технічні характеристики кабелю мережевого обладнання',
        max_length=80,
        blank=True,
    )
    network_filter_material = models.CharField(
        'Матеріал мережевого фільтра',
        max_length=100,
        blank=True,
    )
    network_features = models.TextField(
        'Особливості мережевого обладнання',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    network_additional_features = models.TextField(
        'Додаткові характеристики мережевого обладнання',
        blank=True,
    )
    network_nominal_voltage = models.CharField(
        'Номінальна напруга мережевого обладнання',
        max_length=40,
        blank=True,
    )
    network_protection = models.TextField(
        'Захист мережевого обладнання',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    network_total_power = models.CharField('Сумарна потужність підключеного навантаження', max_length=40, blank=True)
    network_breaker_trip_current = models.CharField(
        'Струм спрацьовування термозапобіжника мережевого обладнання',
        max_length=30,
        blank=True,
    )
    network_barcode = models.CharField('Штрихкод мережевого обладнання', max_length=80, blank=True)
    network_note = models.TextField('Примітка до мережевого обладнання', blank=True)
    thermal_compatibility = models.TextField(
        'Сумісність термопасти',
        blank=True,
        help_text='Якщо значень кілька, розділяйте їх комами.',
    )
    thermal_conductivity = models.CharField('Теплопровідність термопасти', max_length=40, blank=True)
    thermal_weight = models.CharField('Вага термопасти', max_length=30, blank=True)
    thermal_packaging = models.CharField('Тип упаковки термопасти', max_length=40, blank=True)
    thermal_manufacturer = models.CharField('Виробник термопасти', max_length=100, blank=True)
    thermal_country_of_origin = models.CharField('Країна виробництва термопасти', max_length=100, blank=True)
    thermal_barcode = models.CharField('Штрихкод термопасти', max_length=80, blank=True)
    thermal_note = models.TextField('Примітка до термопасти', blank=True)
    # Неопубліковані товари залишаються в адмінці, але не показуються покупцям.
    is_active = models.BooleanField('Опублікований', default=True)
    created_at = models.DateTimeField('Додано', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'товар'
        verbose_name_plural = 'товари'

    def __str__(self):
        return self.name

    @property
    def product_code(self):
        return f'NXS-{self.pk:06d}'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='Товар',
    )
    image_url = models.URLField(
        'URL додаткового фото',
        max_length=1000,
        help_text='Встав повне посилання на зображення, наприклад https://example.com/photo.jpg.',
    )
    alt_text = models.CharField('Опис фото', max_length=200, blank=True)
    position = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ('position', 'pk')
        verbose_name = 'фото товару'
        verbose_name_plural = 'фотографії товару'

    def __str__(self):
        return self.alt_text or f'Фото: {self.product.name}'


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        verbose_name='Користувач',
    )
    phone = models.CharField('Телефон', max_length=30, blank=True)

    class Meta:
        verbose_name = 'профіль покупця'
        verbose_name_plural = 'профілі покупців'

    def __str__(self):
        return f'Профіль: {self.user.username}'


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Товар',
    )
    author_name = models.CharField('Ім’я', max_length=100)
    rating = models.PositiveSmallIntegerField('Оцінка')
    text = models.TextField('Відгук')
    is_approved = models.BooleanField('Опублікований', default=False)
    created_at = models.DateTimeField('Додано', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'відгук'
        verbose_name_plural = 'відгуки'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name='review_rating_between_1_and_5',
            ),
        ]

    def __str__(self):
        return f'{self.author_name} — {self.product.name} ({self.rating}/5)'


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Нове'),
        ('processing', 'В обробці'),
        ('completed', 'Виконане'),
        ('cancelled', 'Скасоване'),
    )

    customer_name = models.CharField('Ім’я та прізвище', max_length=150)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='store_orders',
        null=True,
        blank=True,
        verbose_name='Акаунт покупця',
    )
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Електронна пошта')
    delivery_address = models.CharField('Адреса доставки', max_length=255)
    total = models.DecimalField('Сума замовлення', max_digits=12, decimal_places=2)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'замовлення'
        verbose_name_plural = 'замовлення'

    def __str__(self):
        return f'Замовлення №{self.pk}'

    def cancel(self):
        if not self.pk:
            return False

        with transaction.atomic():
            order = Order.objects.select_for_update().get(pk=self.pk)
            if order.status not in ('new', 'processing'):
                self.status = order.status
                return False

            for item in order.items.all():
                Product.objects.filter(pk=item.product_id).update(
                    stock_quantity=F('stock_quantity') + item.quantity,
                )

            order.status = 'cancelled'
            order.save(update_fields=('status',))
            self.status = order.status
            return True


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Замовлення',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Товар',
    )
    product_name = models.CharField('Назва товару', max_length=200)
    quantity = models.PositiveIntegerField('Кількість')
    unit_price = models.DecimalField('Ціна за одиницю', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'позиція замовлення'
        verbose_name_plural = 'позиції замовлення'

    def __str__(self):
        return f'{self.product_name} × {self.quantity}'
