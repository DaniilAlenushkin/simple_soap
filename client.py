from zeep import Client


def get_documentation(wsdl):
    import operator
    for service in wsdl.services.values():
        print(str(service))
        for port in service.ports.values():
            print(" " * 4, str(port))
            print(" " * 8, "Operations:")
            operations = sorted(port.binding._operations.values(), key=operator.attrgetter("name"))
            for operation in operations:
                print("%s%s" % (" " * 12, str(operation)))
            print("")


if __name__ == '__main__':
    url = 'http://localhost:8000/event/soap?wsdl'
    client = Client(url)
    # client.wsdl.dump()
    get_documentation(client.wsdl)
    print('Получение всех событий')
    events = client.service.read_all_events()
    for event in events:
        print(event.id, event.name, event.participant_number)

    print('\nСоздание события')
    new_event = client.service.create_event('НОВОЕ СОБЫТИЕ', 99)
    print('Создано событие:', new_event.id, new_event.name, new_event.participant_number)

    print('\nПолучение всех событий')
    events = client.service.read_all_events()
    for event in events:
        print(event.id, event.name, event.participant_number)

    print('\nПолучение некоторых событий')
    events = client.service.read_all_events(name='в')
    for event in events:
        print(event.id, event.name, event.participant_number)

    print('\nПолучение события по ID')
    event_id = new_event.id
    event = client.service.read_event(event_id)
    print('Событие:', event_id, event.name, event.participant_number)

    print('\nОбновление события по ID')
    event_id = new_event.id
    update_event = client.service.update_event(event_id, name='ОБНОВЛЕННОЕ СОБЫТИЕ', participant_number=12)
    print('Обновлено событие:', update_event.id, update_event.name, update_event.participant_number)

    print('\nПолучение всех событий')
    events = client.service.read_all_events()
    for event in events:
        print(event.id, event.name, event.participant_number)

    print('\nУдаление события по ID')
    event_id = new_event.id
    delete_id = client.service.delete_event(event_id)
    print('Удалено событие с ID', delete_id)

    print('\nПолучение всех событий')
    events = client.service.read_all_events()
    for event in events:
        print(event.id, event.name, event.participant_number)

    print('\nНекорректные случаи')

    print('\nСоздание события c некорректными типами переданных данных')
    try:
        new_event = client.service.create_event(1, 'wew')
    except Exception as e:
        print(e)

    print('\nПолучение несущетсвующего события по ID')
    event = client.service.read_event(100)
    print('Событие:', event)

    print('\nОбновление несущетсвующего события по ID')
    update_event = client.service.update_event(100, name='ОБНОВЛЕННОЕ СОБЫТИЕ', participant_number=12)
    print('Обновлено событие:', update_event)

    print('\nОбновление события с некорректными типами данных')
    try:
        update_event = client.service.update_event(100, name=1, participant_number="zero")
    except Exception as e:
        print(e)

    print('\nУдаление несущетсвующего события по ID')
    delete_id = client.service.delete_event(100)
    print('Удалено событие с ID', delete_id)
