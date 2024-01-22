# Problem: https://projecteuler.net/problem=79
import requests
from collections import defaultdict, deque

def fetch_logins():
    url = 'https://projecteuler.net/resources/documents/0079_keylog.txt'

    response = requests.get(url)
    file_lines = response.text.strip().split('\n')

    logins = []
    for line in file_lines:
        logins.append(str(line))
    return logins

def topological_sort(graph):
    indegree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1

    queue = deque([u for u in graph if indegree[u] == 0])
    ordered = []
    while queue:
        u = queue.popleft()
        ordered.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return ordered

if __name__ == "__main__":
    logins = fetch_logins()

    graph = defaultdict(set)
    for login in logins:
        for i in range(len(login)):
            if i > 0:
                graph[login[i - 1]].add(login[i])
            if login[i] not in graph:
                graph[login[i]] = set()

    shortest_passcode = topological_sort(graph)

    answer = ''.join(shortest_passcode)
    print(answer)
