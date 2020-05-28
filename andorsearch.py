
'''
Nguyễn Hoàng Thịnh - 17110372
'''
'''
Mô tả: Ta sẽ mô tả bài toán n-queens bằng mảng 1 chiều có n phần tử ( tương ứng với n cột),
mỗi phần tử sẽ có giá trị là hàng sẽ đặt hậu. 
Ta coi trạng thái bang đầu là trên tất cả các cột đều chưa đặt quân hậu nào. 
Ta kí hiệu trạng thái đó bằng mảng 1 chiều như sau: [-1,-1,....,-1] (n phần tử có giá trị
-1 )
Ta quy ước:
GOAL-TEST(state): kiểm tra tổng số cặp hậu ăn nhau. Bằng 0 thì là goal

Action của state: Trên mảng 1 chiều, ta đi từ trái sang phải, 
nếu cột đó chưa được đặt hậu ( nghĩa là có giá trị = -1). 
Ta sẽ lấy ra tất cả các hàng có thể đặt hậu vào cột đó.

RESULTS(state,action): Là kết quả của action vào trong trạng thái hiện tại. 
Kết quả này sẽ cho ra 1 state duy nhất, ta sẽ xem xét 1 kết quả cũng như là 
nhiều kết quả cho phù hợp với mã giả ở trên.
'''

from copy import deepcopy
import time

class Plan:
	def __init__(self, state, action = None, nextPlan = None):
		self.state = state
		self.action = action
		self.nextPlan = nextPlan

	def __str__(self):
		return "Với trạng thái %s ta thực hiện đặt hậu vào hàng %s" % (str(self.state),self.action)

'''
Hàm tạo trạng thái bang đầu là trên tất cả các cột đều chưa đặt quân hậu nào
'''
def create_map(n):
	chessBoard = []
	col = 0
	while col < n:
		chessBoard.append(-1)
		col +=1
	return chessBoard

'''
Hàm kiểm tra trạng thái hiện tại có phải là trạng thái đích hay chưa.
'''
def goal_test(state):
	if state[-1] == -1:
		return False # Tồn tại cột chưa đặt hậu

	# Kiểm tra các cặp hậu ăn nhau
	threat = 0
	n = len(state)
	for i in range(n):
		# state[i] == state[j]: hàng trùng nhau
		# abs(state[i]- state[j]) == j - i: cùng nằm trên đường chéo
		for j in range(i+1,n):
			if state[i] == state[j] or abs(state[i]- state[j]) == j - i:
				threat += 1
	return threat == 0

'''
Hàm sẽ lấy ra tất cả các hàng có thể đặt hậu 
'''
def getActionsOf(state):
	if state[-1] != -1:
		return [] # nghĩa là tất cả các cột đều đã đặt hậu thì không còn hàng nào
				  # trên mỗi cột có thể đặt được nữa

	actions = []
	n = len(state)
	col = state.index(-1) # Lấy ra vị trí phần tử đầu tiên chứa giá trị -1
	if col == 0: # Nếu lấy ra đầu tiên là cột 0 thì tất cả các hàng đều có thể đặt hậu
		return [x for x in range(n)] 

	for i in range(n):
		conflict = False # Tạo một biến cờ để kiểm tra xung đột
		for j in range(n):
			# i == state[j] : cùng hàng
			# col - j == abs(i - state[j]): cùng đường chéo
			if i == state[j] or col - j == abs(i - state[j]):
				conflict = True
		if not conflict:
			actions.append(i)
	return actions

'''
Hàm trả về trạng thái khi đặt action(row) vào state
'''
def RESULTS(state,row):
	col = state.index(-1)
	new = deepcopy(state)
	new[col] = row
	return new





def and_or_graph_search(n):

	def or_search(state,path):
		# Nếu trạng thại hiện tại là goal thì ta trả về một 
		# Plan cùng với trạng thái hiện tại. Nghĩa là đã tìm thấy trạng thái đích
		# thì action = None và nextPlan = None
		if goal_test(state):
			return Plan(state)

		# Nếu trạng thái đã xét qua mà được lặp lại thì không tìm thấy
		if state in path:
			return None

		for action in getActionsOf(state):
			planned = and_search(RESULTS(state,action),path+[state])
			if planned != None:
				# Tạo một plan cho trạng thái hiện tại
				# Khi thực hiện action cho plan ta sẽ nhận được planned
				plan = Plan(state)
				plan.action = action
				plan.nextPlan = planned
				return plan



	def and_search(state,path):
		# Vì ta RESULTS(state,action) là 1 state nên sẽ không có vòng lặp for cho state
		planned = or_search(state,path)
		if planned == None:
			return None
		return planned

	return or_search(create_map(n),[])



def getResults(numOfQueens):

	startTime = time.time()
	solution = and_or_graph_search(numOfQueens)
	ti = time.time() - startTime
	result = {}
	i = 0
	while i< numOfQueens:
		result[i] = solution.action
		i+=1
		solution = solution.nextPlan
	
	return result, ti




