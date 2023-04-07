from spyne import Application, rpc, ServiceBase, Integer, Unicode, Array, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


# Модель Event
class Event(ComplexModel):
    id = Integer
    name = Unicode
    participant_number = Integer

    def __init__(self, id, name, participant_number):
        self.id = id
        self.name = name
        self.participant_number = participant_number


# База данных
events = [Event(1, 'Летний IT-лагерь в Компьютерной Академии', 9),
          Event(2, 'VR Рисование в Виртуальной реальности', 6),
          Event(3, 'Невероятное путешествие по Музею Эмоций', 18),
          Event(4, 'Майские праздники в Музее автомобильных историй', 17),
          Event(5, 'Шоу «Big Stand Up»', 20),
          Event(6, 'Субботник "Под крышей дома моего"', 14),
          Event(7, 'Волонтерский проект "Delevery-бабушка"', 9),
          Event(8, 'Вечеринка "Этонекоронабро"', 16),
          Event(9, 'Большая летняя Спартакиада в Лужниках', 6),
          Event(10, 'Международный день Солнца в Дарвиновском музее', 9)]


# Сервис Event
class EventService(ServiceBase):
    # Создание события
    @rpc(Unicode, Integer, _returns=Event)
    def create_event(ctx, name, participant_number):
        new_event_id = max([event.id for event in events]) + 1
        new_event = Event(new_event_id, name, participant_number)
        events.append(new_event)
        return new_event

    # Получение события по ID
    @rpc(Integer, _returns=Event)
    def read_event(ctx, id):
        for event in events:
            if event.id == id:
                return event
        return None

    # Получение всех событий
    @rpc(Unicode, Integer, _returns=Array(Event))
    def read_all_events(ctx, name=None, participant_number=None):
        if name or participant_number is not None:
            filtered_events = []
            for event in events:
                if name and name in event.name:
                    filtered_events.append(event)
                elif participant_number is not None and  participant_number < event.participant_number:
                    filtered_events.append(event)
            return filtered_events
        return events

    # Обновление события по ID
    @rpc(Integer, Unicode, Integer, _returns=Event)
    def update_event(ctx, id, name=None, participant_number=None):
        for event in events:
            if event.id == id:
                if name:
                    event.name = name
                if participant_number:
                    event.participant_number = participant_number
                return event
        return None

    # Удаление события по ID
    @rpc(Integer, _returns=Integer)
    def delete_event(ctx, id):
        for i, event in enumerate(events):
            if event.id == id:
                del events[i]
                return id
        return None


# Создание приложения и добавление сервиса Event
application = Application([EventService], 'http://example.com/event/soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

# Запуск сервера
if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    server = make_server('localhost', 8000, WsgiApplication(application))
    server.serve_forever()
