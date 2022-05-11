# В терминале набрать pytest
# import pytest
# from main import is_message_ready_to_parse, \
#     get_cars_count, \
#     get_cars_count_by_word, \
#     get_valid_data, \
#     find_range_value

import re
from processor import get_valid_data, get_cars_count

FAKES = [
    'На успенке в сторону РФ стоим с 7 часов утра, только прошли регистрацию ДНР, движения почти нет.',
    '40 минут стоим на Куйбышево в сторону ДНР, ни одной машины не запустили',
    'Только что прошли ДНР-РФ обе границы за 1 час на Новоазовске',
    'Успенка РФ- ДНР 2 часа проходили.',
    'Мариновка днр-рф прошел за 15 минут все',
]

ZERO_CARS = [
    'РФ в сторону мариновки никого',
    'Вознесенка в ДНР пусто',
]

MSGS_WORDS = [
    'Новоазовск из РФ перед заездом пара машин',
]

GOOD_MSG = [
    'Курган 10 перед палкой',
    'Новоазовск РФ ДНР 15 машин',
]

MSGS_WITH_RANGES = [
    'Новоазовск днр- РФ перед палкой порядка 20-25 авто',
    'Мариновка из ДНР в РФ 8-10 машин до шлагбаума ,на нейтралке  столько же',
]


# def test_fakes():
#     for fake_msg in FAKES:
#         assert not is_message_ready_to_parse(fake_msg)
#
#
# def test_zero_cars():
#     for zero_msg in ZERO_CARS:
#         assert not get_cars_count(zero_msg)
#
#
# def test_words_cars_counts():
#     for msg in MSGS_WORDS:
#         assert get_cars_count_by_word(msg) is not None
#
#
# def test_parsed_ok():
#     for msg in GOOD_MSG:
#         assert get_valid_data(msg) is not None


def assertion(result, way, is_cars_zero, car_type=0):
    assert result is not None
    assert result['way'] == way
    assert result['kpp_name']
    if is_cars_zero:
        assert result['cars_num'] == 0
    else:
        assert result['cars_num'] > 0
    assert result['car_type'] == car_type
    assert result['comment']


def test_case_0001():
    msg = 'Три экипажа дпс После кольца кургана'
    result = get_valid_data(msg)
    assert result is None


def test_case_0002():
    msg = 'Успенка ДНР РФ 13 машин'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0003():
    msg = 'Новоазовск ДНР-РФ, перед шлагбаумом 15 машин'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0004():
    msg = 'Мы это сделали!) Всего 9 часов ожидания, и мы проехали. P.S. Новоазовск из ДНР в РФ'
    result = get_valid_data(msg)
    assert result is None


def test_case_0005():
    msg = 'Успенка в ДНР пусто, на нейтралке 2.'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', True)


def test_case_0006():
    msg = 'Новоазовск. Днр -> РФ. Из Днр никого. Нейтралка перед РФ машин 25-30'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', True)


def test_case_0007():
    msg = 'Мариночка перед палкой три авто из РФ в ДНР 🖐️🖐️😂🖐️🖐️'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False)


def test_case_0008():
    msg = 'Ехали через Успенку в Донецк 14 августа. По ошибке на границе на досмотре взяли чужой пакет с вещами. Вдруг здесть есть владелец пакета, напишите в личку.'
    result = get_valid_data(msg)
    assert result is None


def test_case_0009():
    msg = 'На мариновке что нет никого в РФ отзовитесь пожалуйста сколько машин'
    result = get_valid_data(msg)
    assert result is None


def test_case_0010():
    msg = 'Успенка в рф7 машин️'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0011():
    msg = 'Успенка в РФ палка11.'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0012():
    msg = 'Новоазовск ДНР-РФ сразу на въезд. ДНР прошли за 10 мин. На нейтралке 4 машины'
    result = get_valid_data(msg)
    # assertion(result, 'to_rf', True)
    assert result is None


def test_case_0013():
    msg = 'Новоазовск. ДНР-РФ ноль полный. Движение слабое очень.'
    result = get_valid_data(msg)
    assert result is None


def test_case_0014():
    msg = 'Успенка днр -рф 52 ноль забит'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0015():
    msg = 'Мариновка из Донецка ...пр.35 авто.'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0016():
    msg = 'Успенка ы РФ 18 легковых. Фуры за мост'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0017():
    msg = 'Успенка РФ-днр жопа... До гостиницы, стоим...'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False)


def test_case_0018():
    msg = 'Новоазовск, в серой зоне в РФ, машин 20-25'
    result = get_valid_data(msg)
    assert result is None


def test_case_0019():
    msg = 'Курган до поворота и 3 автобуса'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False)


def test_case_0020():
    msg = 'Мариновка -Куйбышево до куста легковые.'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0021():
    msg = 'Куйбышево буфер в Рф пусто'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', True)


def test_case_0022():
    msg = 'Новоазовск. РФ-ДНР свободно'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', True)


def test_case_0023():
    msg = 'Мариновка в РФ вижу 23 легковых,одна грузовая'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0024():
    msg = 'Новоазовск: из РФ в ДНР - 4 на въезд, 1 фура'
    result = get_valid_data(msg)
    # assertion(result, 'to_dnr', False)
    assert result is None


def test_case_0025():
    msg = 'Успенка в РФ середина середина заправки.Фуры далеко за мост.'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False, 0)


def test_case_0026():
    msg = 'Новоазовск перед палкой 0, на серой машин 30, и РФ забита.'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', True)


def test_case_0027():
    msg = 'Курган палка 0 навес 20'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', True)


def test_case_0028():
    msg = 'На Успенке из РФ в ДНР: на въезд 0, под навесом 10'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', True)


def test_case_0029():
    msg = 'Новоазовск в РФ из Днр 25 машин.и под навесом есть.'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0030():
    msg = 'Новоазовск уже машин 70 из ДНР в РФ..; Парадокс!!)); Убрали коммендантский час, сегодня даже лишний ' \
          'день без комменды сделали, чтобы люди пораньше и безпрепятственно типа ехали на выборы, а на таможнях ' \
          'попа!!!..; Полчаса уже стоим тупо без движения!..; Это как вообще??😄😆🤣; Где люди, которые должны были ' \
          'проследить за этой ситуацией?)); А потом скажут, что из ДНР из получивших российские паспорта фига ' \
          'кто проголосовал!!!..'
    result = get_valid_data(msg)
    # assertion(result, 'to_rf', False)
    assert result is None


def test_case_0031():
    msg = 'Мариновка ноль битком'
    result = get_valid_data(msg)
    assert result is None


def test_case_0032():
    msg = 'Мариновка-прошли за 40 мин обе границы ,все спокойно ёжик'
    result = get_valid_data(msg)
    assert result is None


def test_case_0033():
    msg = 'Успенка. Из ДНР в РФ - 25-30, нейтралка забита в 2 ряда'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0034():
    msg = 'Проезд стандартный , Новоазовск-рф буфер пустой'
    result = get_valid_data(msg)
    assert result is None


def test_case_0035():
    msg = 'Успенка На упрощенке в РФ стоим в районе часа, и еще где-то минут 20. Из РФ приблизительно столько же'
    result = get_valid_data(msg)
    assert result is None


def test_case_0036():
    msg = 'Перед шлагбаумом пусто, нейтраль никого. Мариновка из России.'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', True)


def test_case_0037():
    msg = 'На Мариновке в РФ машин 50. Движение идёт, но очень медленно! Стоим 3 часа и ещё машин 15 спереди.'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0038():
    msg = 'Из Донецка в Таганрог через Новоазовск 2ч20 минут'
    result = get_valid_data(msg)
    assert result is None


def test_case_0039():
    msg = 'Мариновка в РФ 23 до шлагбаума. Навес 5.'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0040():
    msg = 'Из РФ в ДНР Успенка 12 машин в терминале'
    result = get_valid_data(msg)
    assert result is None


def test_case_0041():
    msg = 'Курган палка ноль, навес 20 '
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', True)


def test_case_0042():
    msg = 'Успенка в сторону днр, перед шлагбаумом никого. Перед навесом 2 ряда по 10 машин'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', True)


def test_case_0043():
    msg = '1,5 часа обе таможни в сторону ДНР Успенка'
    result = get_valid_data(msg)
    assert result is None


def test_case_0044():
    msg = 'Из РФ в ДНР Новоазовск грузовых штук 100. ДНР практически не работают'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False, 1)


def test_case_0045():
    msg = 'Куйбышево домой грузовых около 30'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False, 1)


def test_case_0046():
    msg = 'Успенка с РФ - до заправки. Стоим глухо. Грузовых 120 насчитали.'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False, 1)


def test_case_0047():
    msg = 'Успенка грузовые из РФ в ДНР до шлагбаума не менее 150 машин'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False, 1)


def test_case_0048():
    msg = 'Кто знает, почему на Новоазовске не работают таможенники на въезд грузовых? Очередь грузовых на въезд 3 км. С чем это связано?'
    result = get_valid_data(msg)
    assert result is None


def test_case_0049():
    msg = 'Успенка рф-днр 10 машин за поворотом'
    result = get_valid_data(msg)
    print(result)
    assert result['cars_num'] > 30


def test_case_0050():
    msg = 'Успенка в РФ шлагбаум 0, навес 11, нейтральная в 2 рчда'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', True)


def test_case_0051():
    msg = 'Успенка. Из РФ в ДНР. Легковых - 0, грузовых - 104'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', True)


def test_case_0052():
    msg = 'В 3.30 на Успенке было пусто, пишут. А вечером полно. Всё может измениться в один момент'
    result = get_valid_data(msg)
    assert result is None


def test_case_0053():
    msg = 'Успенка таже история, 2 часа в таможне. Продвинулись на 3 кузова.'
    result = get_valid_data(msg)
    assert result is None


def test_case_0054():
    msg = 'Новоазовск в РФ палка 20 0/5 маш.'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0055():
    msg = 'Выезд из ДНР в РФ через успенку. Очередь примерно часа на 4'
    result = get_valid_data(msg)
    assert result is None


def test_case_0056():
    msg = 'Ищу 1 место сегодня ночью для мужа с Мелового до Донецка или до Успенки. Пишите в лс.'
    result = get_valid_data(msg)
    assert result is None


def test_case_0057():
    msg = 'Новоазовск РФ-днр на машин до  поворота на границу'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False)


def test_case_0058():
    msg = 'Новоазовск:ДНР -> РФ - 15 машинМного фур.'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0059():
    msg = 'На успенке со стороны России авто штук 60'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False)


def test_case_0060():
    msg = 'Успенка в РФ- 0 забит'
    result = get_valid_data(msg)
    assert result is None


def test_case_0061():
    msg = '8:10 Успенка из РФ в ДНР пару машин на таможне'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False)


def test_case_0062():
    msg = 'Из РФ в ДНР на Мариновке нет машин перед палкой, под навесом 5 машин.'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', True)


def test_case_0062():
    msg = 'Из 🇷🇺 на Новоазовск до лукоила'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False)


def test_case_0063():
    msg = 'В РФ на Мариновке 43 автобуса'
    result = get_valid_data(msg)
    assert result is None


def test_case_0064():
    msg = 'В рф на Новоазовске легковых одна фур штук 30-40'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0065():
    msg = 'Со стороны РФ Успенка очередь заходит за поворот'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False)


def test_case_0066():
    msg = 'Мариновка 0 перед палкой 3 под навесом'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', True)


def test_case_0067():
    msg = 'Успенка из РФ. 35 мин 2 таможни'
    result = get_valid_data(msg)
    assert result is None


def test_case_0068():
    msg = 'Ноль на Новоазовск забит в сторону Рф'
    result = get_valid_data(msg)
    assert result is None


def test_case_0069():
    msg = 'Мариновка из ДНР в РФ 4 машины. В нейтралке 2'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False)


def test_case_0070():
    msg = 'Успенка 25+ между границами'
    result = get_valid_data(msg)
    assert result is None


def test_case_0071():
    msg = 'Да потому, что еще 2 месяца назад на новоазовск все бездумно ломанулись и очереди ' \
          'были больше, чем на успенке.'
    result = get_valid_data(msg)
    assert result is None


def test_case_0072():
    msg = 'Успенка-Донецк...скользко...40-60..км'
    result = get_valid_data(msg)
    assert result is None


def test_case_0073():
    msg = 'На мариновка сразу на заезд,но серая зона забита,снег не чищен,никто не может проехать,' \
          'Все стоят в одной очереди и фуры и автобусы,и машины.Говорят,' \
          'что автобусы впереди с 12 дня стоят,и до сих пор там.'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', True, 0)


def test_case_0074():
    msg = "В сторону Мариновки поехала снегоуборочная машина, а инвалиды', рожающие', нетерпеливые сделали 2 ряд."
    result = get_valid_data(msg)
    assert result is None


def test_case_0075():
    msg = 'Приехали на успенку в 1:50 (стали на гостинице) сейчас только прошли рф, стоим метров 30 от Дьюти фри'
    result = get_valid_data(msg)
    assert result is None


def test_case_0076():
    msg = 'А вообще, /оффтоп/, на Успенку я забил ездить уже 2 года как. ' \
          'На других КПВВ тоже не сахар, но Успенка ВСЕГДА самая медленная таможня.'
    result = get_valid_data(msg)
    assert result is None


def test_case_0077():
    msg = 'РФ в ДНР На успенке все так же до поворота... Около 17 машин. Пока стоим. Впускают фуры'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False, 0)


def test_case_0078():
    msg = 'Отвечаю как допога с Новоазовска в Донецк, первые 30 км пути гололед частично, не разгоняйтесь, ' \
          'затем дорога почти чистая и посыпанная, за Старобешево до Донецка опять ' \
          'лед, при мне с кювета машину доставали, так что осторожно'
    result = get_valid_data(msg)
    assert result is None


def test_case_0079():
    msg = 'Заберу с Успенки 2-3 человека. Пустой багажник. В сторону Енакиево.'
    result = get_valid_data(msg)
    assert result is None


def test_case_0080():
    msg = 'На трассе Успенка- Донецк дтп ,затор на трассе,можно объехать .За заправкой в Кутейников ' \
          'уходите налево через Комсомольское,Старобешево на Донецк но скользкая,будьте внимательней'
    result = get_valid_data(msg)
    assert result is None


def test_case_0081():
    msg = 'Стоим с 16:00 на Матвеев Кургане, от заправки проехали метров 300'
    result = get_valid_data(msg)
    assert result is None


def test_case_0082():
    msg = 'Из РФ в ДНР проехал по Успенке за 35-40 минут'
    result = get_valid_data(msg)
    assert result is None


def test_case_0083():
    msg = 'Успенка 3 машины на въезд в РФ, фур до фига, ноль забит'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False, 0)


def test_case_0084():
    msg = 'Успенка в РФ, пеших много, человек 30-40, ждем'
    result = get_valid_data(msg)
    assert result is None


def test_case_0085():
    msg = 'На успенке очередь грузовых 2-3 км'
    result = get_valid_data(msg)
    assert result is None


def test_case_0086():
    msg = 'Успенка из РФ в ДНР на палке 12 машин , под навесом забито машин 40 , грузовиков немеренно'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', False, 0)


def test_case_0087():
    msg = 'Люди, нужна помощь! Кто может забрать 2 маленькие посылочки из магазина "Пятёрочка" в с. Куйбышево'
    result = get_valid_data(msg)
    assert result is None


def test_case_0088():
    msg = 'Мариновка в РФ. Движемся по 5 авто за пол часа. Очередь начинается дальше конца спуска'
    result = get_valid_data(msg)
    assert result is None


def test_case_0089():
    msg = 'Все равно не пускают, военнообязанных, людей пускают из РФ в ДНР по 10-20 человек, Успенка'
    result = get_valid_data(msg)
    assert result is None


def test_case_0090():
    msg = 'Папа ехал в сторону успенки, вот сейчас (ему 59) его пропустили через посты, но мужчин призывного разворачивают. Что на самой таможне-неизвестно.'
    result = get_valid_data(msg)
    assert result is None


def test_case_0091():
    msg = 'Новоазовск из РФ пусто. Из ДНР на палке пусто, на нейтралке около 10 легковых'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', True, 0)


def test_case_0092():
    msg = '... мужчин не выпускают из ДНР в РФ и обратно на Успенке , 16 - 65 лет . Или уже пропускают ?'
    result = get_valid_data(msg)
    assert result is None


def test_case_0093():
    msg = 'успенка Подъехали были 13е , через 2 мин запустили 10 машин...'
    result = get_valid_data(msg)
    assert result is None


def test_case_0094():
    msg = 'Успенка из РФ в ДНР.Запустили сразу, очередь в 2 ряда по 10-13 машин.'
    result = get_valid_data(msg)
    assertion(result, 'to_dnr', True, 0)


def test_case_0095():
    msg = 'на Новоазовске 70 машин было 1,5 часа назад, большинство из Мариуполя, мчсники посоветовали на Успенку или Мариновку ехать, т.к. их долго проверяют'
    result = get_valid_data(msg)
    assert result is None


def test_case_0096():
    msg = 'На Успенке в 8-30 было 45 авто. Очередь почти не продвигается уже вот как 3 часа.'
    result = get_valid_data(msg)
    assert result is None


def test_case_0097():
    msg = 'На успенке пишут 70-60машин'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False, 0)


def test_case_0098():
    msg = 'Одна мариновка что ли работает??)))) Остальные спят? ....'
    result = get_valid_data(msg)
    assert result is None


def test_case_0099():
    msg = 'На Успенке ЦРБ работает 24/7'
    result = get_valid_data(msg)
    assert result is None


def test_case_0100():
    msg = 'Успенка в РФ машин 40+, пеших 100+'
    result = get_valid_data(msg)
    assertion(result, 'to_rf', False, 0)


def test_case_0101():
    msg = 'Успенка стоит. На пешем переходе человек 200.'
    result = get_valid_data(msg)
    assert result is None


def test_case_0102():
    msg = 'Успенка в РФ больше 2-х часов не двигается'
    result = get_valid_data(msg)
    assert result is None


def test_case_0103():
    msg = ''
    result = get_valid_data(msg)
    # assert result is None


def run_tests():

    test_case_0103()
    # test_case_0102()
    # test_case_0101()
    # test_case_0100()
    # test_case_0099()
    # test_case_0098()
    # test_case_0097()
    # test_case_0096()
    # test_case_0095()
    # test_case_0094()
    # test_case_0093()
    # test_case_0092()
    # test_case_0091()
    # test_case_0090()
    # test_case_0089()
    # test_case_0088()
    # test_case_0087()
    # test_case_0086()
    # test_case_0085()
    # test_case_0084()
    # test_case_0083()
    # test_case_0082()
    # test_case_0081()
    # test_case_0080()
    # test_case_0079()
    # test_case_0078()
    # test_case_0077()
    # test_case_0076()
    # test_case_0075()
    # test_case_0074()
    # test_case_0073()
    # test_case_0072()
    # test_case_0071()
    # test_case_0070()
    # test_case_0069()
    # test_case_0068()
    # test_case_0067()
    # test_case_0066()
    # test_case_0065()
    # test_case_0064()
    # test_case_0063()
    # test_case_0062()
    # test_case_0061()
    # test_case_0060()
    # test_case_0059()
    # test_case_0058()
    # test_case_0057()
    # test_case_0056()
    # test_case_0055()
    # test_case_0054()
    # test_case_0053()
    # test_case_0052()
    # test_case_0051()
    # test_case_0050()
    # test_case_0049()
    # test_case_0048()
    # test_case_0047()
    # test_case_0045()
    # test_case_0046()
    # test_case_0044()
    # test_case_0043()
    # test_case_0041()
    # test_case_0040()
    # test_case_0039()
    # test_case_0038()
    # test_case_0036()
    # test_case_0035()
    # test_case_0034()
    # test_case_0033()
    # test_case_0032()
    # test_case_0031()
    # test_case_0030()
    # test_case_0029()
    # test_case_0028()
    # test_case_0027()
    # test_case_0026()
    # test_case_0025()
    # test_case_0024()
    # test_case_0023()
    # test_case_0022()
    # test_case_0021()
    # test_case_0020()
    # test_case_0019()
    # test_case_0018()
    # test_case_0017()
    # test_case_0016()
    # test_case_0015()
    # test_case_0014()
    # test_case_0013()
    # test_case_0012()
    # test_case_0011()
    # test_case_0010()
    # test_case_0009()
    # test_case_0008()
    # test_case_0007()
    # test_case_0006()
    # test_case_0005()
    # test_case_0004()
    # test_case_0003()
    # test_case_0002()
    # test_case_0001()

    ...
    print('\n *** ALL TESTS FINISHED ***')

    # test_case_0037()  # Много цифр


"""
Проблемные:
слишком запутано:
 
 Новоазовск. Рф- ДНР никого. Днр- РФ никого, в промзоне машин 10-15


Инфы нет, но одна цифра

 7	0	Мариновка из рф в днр очень медлено, всего 5 машин час стоим смена дыбилов !
 
 
Не распознается какая цифра принадлежит к легковые:
 
 'Из Куйбышево в ДНР 4 легковые, 2 фуры, подтянулся автобус'


 
"""
