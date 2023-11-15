def _is_all_in_seed(urls_list, seed):
		if set(urls_list).issubset(seed):
			return True
		else:
			return False
main = [1,2,3,4]
sub = [2,1,17]

print( _is_all_in_seed(sub, main))
