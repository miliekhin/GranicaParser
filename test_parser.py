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
    assertion(result, 'to_rf', True)


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
    assertion(result, 'to_rf', False, 1)


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
    assert result is None


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


def run_tests():

    test_case_0060()
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
    # test_case_0042()
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

    print('\n ***ALL TESTS FINISHED***')

    # test_case_0037()  # Много цифр

"""
Проблемные:
слишком запутано:
 
 Новоазовск. Рф- ДНР никого. Днр- РФ никого, в промзоне машин 10-15


Инфы нет, но одна цифра

 7	0	Мариновка из рф в днр очень медлено, всего 5 машин час стоим смена дыбилов !

 
"""