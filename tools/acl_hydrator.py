import os
import yaml
import click

'''what we are trying to do here is load an acl which contains either single subnets or references to objects which
  in turn also contain either single subnets or references to other objects. The goal is to replace all references
  with a list of concrete subnets so that it can be written out into a new file for further processing'''


@click.command()
@click.option('--acl', default='../rulesets/example_ACL.yaml', help='The input ACL with relative path.')
@click.option('--object_dir', default='../objects/', help='Relative path to objects')
@click.option('--hydrated_file', default='./hydrated.yaml', help='Output file after hydration')
def main(acl, object_dir, hydrated_file):
    print_title()

    '''open the main ACL file'''
    with open(acl, 'r') as infile:
        master_acl = yaml.load(infile)

    '''open and concatenate all objects in the objects folder into one dictionary'''
    master_object = {}
    for filename in os.listdir(object_dir):
        with open(object_dir + filename) as infile:
            for entry in yaml.safe_load_all(infile):
                master_object.update(entry)

    new_rule_set = load_rulesets(master_acl, master_object)

    for i,v in enumerate(new_rule_set['ACL']['rules']):
        print(new_rule_set['ACL']['rules'][i].items())

    # for rule in new_rule_set['ACL']['rules']:
    #      print(rule['description'])
    #      print(rule['_belongs_to'])
    #      print(rule['source'])
    # #     print(rule['sport'])
    #      print(rule['dest'])
    # #     print(rule['dport'])
    # #     print(rule['proto'])
    # #     print(rule['action'])
    # # write_rule_set(rule_set, hydrated_file)
    # print(new_rule_set)


def print_title():
    print('------------------------------')
    print('      ACL HYDRATOR APP')
    print('------------------------------')


def load_rulesets(master_acl, master_object):
    '''create copy of original and later only replace the bits that get hydrated. All the descriptions etc remain
    untouched'''

    new_acl = master_acl

    for index, rule in enumerate(master_acl['ACL']['rules']):

        source, dest, sport, dport, proto = str(rule['source']), str(rule['dest']), \
                                            str(rule['sport_start']), str(rule['dport_start']), str(rule['proto'])

        '''check whether there is a further reference via curly brackets to another object, if so invoke
        the recursive load_object function which returns with the full list '''

        if source[0:2] == '{{':
            object_name = source
            list_of_objects = load_object(object_name, master_object)
            new_acl['ACL']['rules'][index]['source'] = list_of_objects

        ''' do the above for the other four tuples i.e. ports, dest etc'''

        if dest[0:2] == '{{':
            object_name = dest
            list_of_objects = load_object(object_name, master_object)
            new_acl['ACL']['rules'][index]['dest'] = list_of_objects

        if sport[0:2] == '{{':
            object_name = sport
            list_of_objects = load_object(object_name, master_object)
            new_acl['ACL']['rules'][index]['sport_start'] = list_of_objects

        if dport[0:2] == '{{':
            object_name = dport
            list_of_objects = load_object(object_name, master_object)
            new_acl['ACL']['rules'][index]['dport_start'] = list_of_objects

        if proto[0:2] == '{{':
            object_name = proto
            list_of_objects = load_object(object_name, master_object)
            new_acl['ACL']['rules'][index]['proto'] = list_of_objects

    return new_acl


def load_object(object_name, master_object):
    ''' list_of_objects can either be another reference, then this function will calls itself again, if not
         then we return the actual list'''

    key = object_name.strip('{} ')
    network_objects = []

    if type(master_object[key]) == str:
        network_objects = master_object[key]
    elif type(master_object[key]) == list:
        for network_object in master_object[key]:
            if network_object[0:2] == '{{':
                temp_object = load_object(network_object, master_object)
                network_objects.append(temp_object)
            else:
                network_objects.append(network_object)

    return network_objects


if __name__ == '__main__':
    main()
