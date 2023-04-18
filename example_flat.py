import json
import random
import os
import flatbuffers
import persistent_state.Persistent
import persistent_state
import PersistentStruct


class Outbox:
    """
    some dummy class to simulate the outbox just write the data to a file
    """

    def __init__(self, url):
        self._file_path = url

    def send_cloud_message(self, data):
        with open(self._file_path, 'w') as file:
            file.write(data)



class Database:
    """
    some dummy class to simulate the database just write the data to a file
    """

    def __init__(self, url):
        self._file_path = url

    def get_edge_module_storage(self, edge_module_name):
        with open(self._file_path, 'rb') as file:
            buffer = file.read()
            buffer = bytearray(buffer)
        return buffer

    def save_edge_module_storage(self, data):
        with open(self._file_path, 'wb') as file:
            file.write(data)


class GPSMessage:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


class DataProvider:

    def __init__(self):
        self.messages = []
        self.generate_messages()

    def get_gps_messages_of_front(self):
        return self.messages

    def is_empty(self, message_type):
        return len(self.messages) == 0

    def generate_messages(self):
        number_of_messages = random.randint(0, 10)
        for i in range(number_of_messages):
            self.messages.append(GPSMessage(random.random(), random.random()))

    def pop(self, message_type):
        self.messages = []


def read_persistent_data(buffer):
    """
    reads a byte buffer and returns the data
    :param buffer: a list of bytes
    :return:
    """
    data = persistent_state.Persistent.Persistent.GetRootAsPersistent(buffer)
    return data.SumLat(), data.SumLon(), data.Counter()


def write_persistent_data(sum_lat, sum_lon, counter):
    """
    writes the data to a byte buffer
    :param sum_lat:
    :param sum_lon:
    :param counter:
    :return:
    """
    builder = flatbuffers.Builder(0)
    persistent_state.Persistent.PersistentStart(builder)
    persistent_state.Persistent.PersistentAddSumLat(builder, sum_lat)
    persistent_state.Persistent.PersistentAddSumLon(builder, sum_lon)
    persistent_state.Persistent.PersistentAddCounter(builder, counter)
    data = persistent_state.Persistent.PersistentEnd(builder)
    builder.Finish(data)
    return builder.Output()


def read_persistent(buffer):
    n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buffer, 0)
    x = PersistentStruct.PersistentStruct()
    x.Init(buffer, n)
    return x

def write_persistent(lat, lon, counter):
    builder = flatbuffers.Builder(0)
    pos = PersistentStruct.CreatePersistentStruct(builder, lat, lon, counter)
    builder.Finish(pos)
    return builder.Output()

def run(persistent_data: Database,data_provider:DataProvider, outbox: Outbox):
    """

    :param persistent_data:  normally a database but for simplicity we used a file path
    :param outbox: normally a database but for simplicity we used a file path
    :return:
    """
    _edge_module_name = 'example'
    message_type = 1
    sum_lat = 0.
    sum_lon = 0.
    counter = 0

    # get peristent data and check if available
    storage = persistent_data.get_edge_module_storage(_edge_module_name)

    if len(storage) != 0:
        # read sbyte buffer with flat_buffers
        print(" we have a persistent data ")
        x = read_persistent(storage)
        sum_lat = x.SumLat()
        sum_lon = x.SumLon()
        counter = x.Counter()
        print(f"sum lon = {sum_lon} sum_lat = {sum_lat} counter = {counter}")
    else:
        print("no peristent data available")

    if not data_provider.is_empty(message_type) :
        # get first container of messages
        messages = data_provider.get_gps_messages_of_front()
        for message in messages :
            sum_lat = sum_lat + message.lat
            sum_lon = sum_lon + message.lon
            counter = counter + 1
        print( f"sum lon = {sum_lon} sum_lat = {sum_lat} counter = {counter}")
        data_provider.pop( message_type )
    # read sensor messages from data provider
    aver_lon = sum_lon / counter
    aver_lat = sum_lat / counter

    print(f"average lon = {aver_lon} average lat = {aver_lat} ")

    output_buffer = write_persistent(sum_lat, sum_lon, counter)
    database.save_edge_module_storage(output_buffer)

    dictionary = {
        "average lon": aver_lon,
        "average lat": aver_lat
    }
    json_object = json.dumps(dictionary, indent=4)
    outbox.send_cloud_message(json_object)

    print("edge module finished")


if __name__ == '__main__':
    # create a data provider


    data_provider = DataProvider()
    # create a database
    database = Database('database.bin')
    # create a outbox
    outbox = Outbox('outbox.bin')
    # run the example
    run(database, data_provider, outbox)