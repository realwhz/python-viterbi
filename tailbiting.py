import copy

class codec(object):
    constraint_len = 0;
    num_ports = 0
    gen_polys = list()
    init_metrics = list()
    def __init__(self, constraint_len, num_ports, gen_polys):
        self.constraint_len = constraint_len
        self.num_ports = num_ports
        self.gen_polys = gen_polys
        self.init_metrics = [0] * 2**(constraint_len-1)
    def encode(self, input):
        register = input[len(input)-(self.constraint_len-1) : len(input)-1]
        output = list()
        for x in input:
            register.insert(0, x)
            for i in range(self.num_ports):           
                tmp = sum(g*r for g, r in zip(self.gen_polys[i], register))
                output.append(tmp % 2)
            register = register[0:self.constraint_len-1]
        return output
    def decode(self, input):
        sur_state, sur_paths = self.viterbi_trial(input)
        sur_path, decoded_bits = self.trace_back(sur_state, sur_paths)
        if sur_path[0] == sur_path[-1]:
            return decoded_bits
        else:
            sur_state, sur_paths = self.viterbi_trial(input)
            sur_path, decoded_bits = self.trace_back(sur_state, sur_paths)
            if sur_path[0] == sur_path[-1]:
                return decoded_bits
            else:
                sur_path, decoded_bits = self.trace_back(sur_path[0], sur_paths)
                return decoded_bits
    def viterbi_trial(self, input):
        sur_paths = [[] for s in range(2**(self.constraint_len-1))]
        cur_states = list(range(2**(self.constraint_len-1)))
        state_metrics = copy.deepcopy(self.init_metrics)
        time_len = len(input)//self.num_ports
        for t in range(time_len):
            tmp_state_metrics = copy.deepcopy(state_metrics)
            for s in cur_states:
                pre1 = (s & ~(1 << self.constraint_len-2)) << 1
                pre2 = pre1 + 1
                register1 = dec2bin(pre1, self.constraint_len-1)
                register1.insert(0, s >> self.constraint_len-2)
                register2 = dec2bin(pre2, self.constraint_len-1)
                register2.insert(0, s >> self.constraint_len-2)
                out1 = []
                out2 = []
                for i in range(self.num_ports):                   
                    tmp = sum(g*r for g, r in zip(self.gen_polys[i], register1))
                    out1.append(tmp % 2)                    
                    tmp = sum(g*r for g, r in zip(self.gen_polys[i], register2))
                    out2.append(tmp % 2)
                out1 = [1.0-2.0*x for x in out1]
                out2 = [1.0-2.0*x for x in out2]
                chunk = input[t*self.num_ports:(t+1)*self.num_ports]
                b1 = sum(-x*y for x, y in zip(out1, chunk))
                b2 = sum(-x*y for x, y in zip(out2, chunk))
                if state_metrics[pre1]+b1 < state_metrics[pre2]+b2:
                    sur_paths[s].append(pre1)
                    tmp_state_metrics[s] = state_metrics[pre1]+b1
                else:
                    sur_paths[s].append(pre2)
                    tmp_state_metrics[s] = state_metrics[pre2]+b2
            state_metrics = copy.deepcopy(tmp_state_metrics)
        sur_state = state_metrics.index(min(state_metrics))
        self.init_metrics = copy.deepcopy(state_metrics)
        return (sur_state, sur_paths)
    def trace_back(self, sur_state, sur_paths):
        sur_path = [sur_state]
        decoded_bits = []
        s = sur_state
        for t in reversed(range(len(sur_paths[sur_state]))):
            decoded_bits.insert(0, sur_state >> self.constraint_len-2)
            s = sur_paths[sur_state][t]
            sur_path.insert(0, s)
            sur_state = s
        return (sur_path, decoded_bits)

def dec2bin(x, width):
    out = []
    for i in range(width):
        out.append(x & 1)
        x >>= 1
    out.reverse()
    return out
