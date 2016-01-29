import praw
import json

USER_NAME = 'fultonla-bot'
PASSWORD = '93b8yctV&^VYf2'

def main():
	# post_id = '4399io'
	post_id = '439xuh'

	print "Fetching comments. This may take a few minutes..."
	comments = get_all_comments(post_id)
	print "Done fetching comments."

	comments.sort(key=lambda c: c['created'])

	with open(post_id + '.json', 'w') as outfile:
		json.dump(comments, outfile)

def get_all_comments(submission_id):
	r = praw.Reddit('comment scraper')
	r.login(USER_NAME, PASSWORD, disable_warning=True)
	
	submission = r.get_submission(submission_id=submission_id)
	submission.replace_more_comments(limit=None, threshold=0)

	flat_comments = praw.helpers.flatten_tree(submission.comments)
	return [comment_to_dict(c) for c in flat_comments
				if isinstance(c, praw.objects.Comment)]

def comment_to_dict(comment):
	author = comment.author

	return {
		'id': comment.id,
		'parent_id': comment.parent_id.split('_')[-1],
		'score': comment.score,
		'created': comment.created,
		'author_name': author.name if author else None,
		'replies': [c.id for c in comment._replies],
	}		

if __name__ == "__main__":
	main()