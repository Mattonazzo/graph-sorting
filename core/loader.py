import core.graph, core.stack

def load_graphs_from_file (textfile: str) -> dict:
    s = core.stack.Stack ()
    graphs_list = {}
    f_in = open (textfile, "r")
    for line in f_in:
        line = line.strip()
        lst_line = line.split()
        if lst_line [1] == "start":
            s.push (lst_line[0]) # the graph's name
            graphs_list[s.peek()] = core.graph.Graph ()
        elif lst_line [1] == "->":
            if s.isEmpty():
                raise RuntimeError (f"Input file missing of a start statement before {line = }")
            graphs_list[s.peek()].add_vertex(lst_line[0])
            i = 2
            while i < len (lst_line):
                graphs_list[s.peek()].add_edge(lst_line[0],lst_line[i])
                i += 1
        elif lst_line [1] == "stop":
            if s.isEmpty():
                raise RuntimeError (f"Input file is missing of a start statement before {line = }")
            # stop = 
            s.pop()
        else:
            raise ValueError (f"{lst_line[1]} isn't the right statement: only 'start', 'stop', and '->' are accepted")
    f_in.close()
    if s.isEmpty():
        return graphs_list
    else:
        raise RuntimeError (f"Input file, on {s.peek()} graph, is missing of a stop statement")
