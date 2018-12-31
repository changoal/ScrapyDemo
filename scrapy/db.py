import pymongo
import os

client = pymongo.MongoClient('localhost', 27017)
collection = client['wallhaven']['wall']
master_collection = client['wallhaven']['master']

error_ids = list()


def test_update_data():
    data = test_collection.find_one()
    data['Views'] = int(data['Views'])
    master_collection.find_one_and_update({
        '_id': data['_id']
    }, {
        '$set': {
            'Views': int(data['Views']),
            'favourites': int(data['favourites']),
        }
    })

    data = master_collection.find_one()
    print(data)


def update_data():
    for data in collection.find():
        try:
            data['width'] = str2int(data['width'])
            data['height'] = str2int(data['height'])
            data['favourites'] = str2int(data['favourites'])
            data['Views'] = str2int(data['Views'])
            master_collection.insert_one(data)
        except Exception as e:
            error_ids.append(data['_id'])


def str2int(data):
    """
    str转int
    """
    data = str(data)
    data = data.replace(" ", "")
    data = data.replace(",", "")
    return int(data)


def drop_master_collection():
    """
    删除 master 集合
    """
    master_collection.drop()


def main():
    """
    转化数据
    """
    update_data()
    if error_ids:
        error_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'error.txt')
        with open(error_file, 'w') as f:
            f.write(error_ids)


if __name__ == "__main__":
    # for data in master_collection.find().sort('favourites', -1).limit(10):
    #     print("https://{url}".format(url=data['img_url']))
    # print(master_collection.find().sort('Views', -1).limit(1))
    cursor = master_collection.find({'_id': '-1'})
    if cursor.count():
        print(cursor.comment)
    else:
        print("not found")