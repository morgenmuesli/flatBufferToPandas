
import edge_module_database
import edge_module_data_provider
import edge_module_outbox
import json

def run( peristent_data : edge_module_database.edge_module_database,
         data_provider : edge_module_data_provider.edge_module_data_provider,
         outbox : edge_module_outbox.edge_module_outbox ) :
    edge_module_name = 'example'
    message_type = 1
    sum_lat = 0.
    sum_lon = 0.
    counter = 0

    # get peristent data and check if available
    storage = peristent_data.get_edge_module_storage( edge_module_name )
    if len(storage) != 0 :
        # read sbyte buffer with flat_buffers
        print(" we a persistent data ")
    else:
        print("no peristent data available")

    # read sensor messages from data provider
    if not data_provider.is_empty(message_type) :
        # get first container of messages
        messages = data_provider.get_gps_messages_of_front()
        for message in messages :
            sum_lat = sum_lat + message.lat
            sum_lon = sum_lon + message.lon
            counter = counter + 1
        print( f"sum lon = {sum_lon} sum_lat = {sum_lat} counter = {counter}")
        data_provider.pop( message_type )

    # calculate average
    aver_lon = sum_lon/counter
    aver_lat = sum_lat/counter

    print( f"average lon = {aver_lon} average lat = {aver_lat} ")
    print( f"number of avalible message_containers = {data_provider.get_num_of_time_span_messages(message_type)}")
    # send result to cloud
    dictionary = {
        "average lon": aver_lon,
        "average lat": aver_lat
    }
    json_object = json.dumps(dictionary, indent=4)

    outbox.send_cloud_message(json_object)

    #write peristent data to buffer

    print("edge module finished")

