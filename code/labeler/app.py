from flask import Flask, render_template, request, jsonify
import pymongo


app = Flask(__name__)
app.config.from_object('config')

client = pymongo.MongoClient('localhost', 27017)
db = client.phronesis_food_photos

top_categories = [
    'coffee', 'beer', 'burrito', 'pizza', 'salad',
    'diet soda', 'veggie sausage', 'chips', 'red curry',
    'cheese sandwich', 'apple', 'juice', 'flax seed oil', 'pasta',
    'soup', 'pad thai', 'tea', 'tacos', 'quesadilla'
]

@app.route('/')
def index():
    images = db.clean_photo_data.find({'category': {'$exists': False}}, {'_id': 0}).sort('timestamp').limit(200)
    # images = db.clean_photo_data.find({'category': {'$in': top_categories}}).sort('category')
    return render_template('main.html', images=images)


@app.route('/photo', methods=['PUT'])
def photo():
    if request.method == 'PUT':
        id = request.form['id']
        category = request.form['category']
        db.clean_photo_data.update(
            {'id': id}, {'$set': {'category': category}})
        return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run()