from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    #
    return jsonify(POSTS)

@app.route('/api/posts', methods=['POST'])
def add_posts():
    if request.method == 'POST':
            # Get the new book data from the client
        data = request.get_json()

            # Generate a new ID for the post

        new_post = {"id": len(POSTS)+1,
                    "title": data["title"],
                    "content": data["content"]
                    }

        # Add the new book to our list
        POSTS.append(new_post)
        print("HERE")
        # Return the new post data to the client
        return jsonify(new_post), 201
    else:
        # Handle the GET request
        return jsonify(POSTS)


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    # Find the book with the given ID
    deletable_post = None
    for post in POSTS:
        if post["id"] == post_id:
            deletable_post = post
            break

    if deletable_post is None:
        return jsonify({"error":"post not found"}), 404

    POSTS = [post for post in POSTS if post["id"] != post_id]
    return jsonify({"message": f"Post {post_id} deleted successfully"}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update(post_id):
    """Update a blog post by ID."""
    global POSTS
    post_to_update = next((post for post in POSTS if post['id'] == post_id), None)
    if post_to_update is None:
        return jsonify({"error": "Post not found"}), 404
    data = request.get_json()
    if 'title' in data:
        post_to_update['title'] = data['title']
    if 'content' in data:
        post_to_update['content'] = data['content']

    return jsonify({
        "id": post_to_update['id'],
        "title": post_to_update['title'],
        "content": post_to_update['content']
    }), 200



@app.route('/api/posts/search', methods=['GET'])
def search_by_title():
    """Search for posts by title or content."""
    search_parameter = request.args.get('query', '').strip().lower()
    matching_posts = [post for post in POSTS if search_parameter in
                      post['title'].lower() or search_parameter in
                      post['content'].lower()]
    if matching_posts:
        return jsonify(matching_posts)
    else:
        return jsonify({"error": "Post not found "}), 404


@app.route('/api/posts', methods=['GET'])
def get_sorted_posts():
    """Get all posts sorted by title or content."""
    sort_by = request.args.get('sort', '').strip().lower()
    direction = request.args.get('direction', 'asc').strip().lower()

    valid_sort_fields = {'title', 'content'}

    if sort_by in valid_sort_fields:
        reverse_order = direction == 'desc'
        sorted_posts = sorted(POSTS, key=lambda post: (post[sort_by] or "").lower(), reverse=reverse_order)
    else:
        sorted_posts = POSTS
    return jsonify(sorted_posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
