
class VMBase:
    _stack_top: int = 0  # 寄存器 栈指针 指向栈下一个最顶端的基址
    _local: int = 0  # 指向local的基址
    _argument: int = 0
    _this: int = 0
    _that: int = 0
    ip: int  # 指令索引
    _current_instrument = []
    _temp = None  # 储存临时值

    _ram: [int] = []

    _arriveEnd: bool = False

    def _execute_arithmetic(self, command: str):
        raise NotImplementedError

    def _execute_push(self, content):
        raise NotImplementedError

    def _execute_pop(self, content):
        raise NotImplementedError

    def _launch(self):
        raise NotImplementedError

    def _load(self):
        raise NotImplementedError

    def _run(self):
        raise NotImplementedError


class VM(VMBase):
    def __init__(self, ramsize: int):
        self._stack_top = 0
        self._local = 0
        self._argument = 0
        self.ip = 0
        self._ram = [None for _ in range(ramsize)]
        self._instruction_ram = []
        self._instruction_address = {}

    def _execute_arithmetic(self, commmand: str):
        sp = self._stack_top
        if commmand == "add":
            self._ram[sp - 2] = int(self._ram[sp - 2]) + int(self._ram[sp - 1])
            sp -= 1
        elif commmand == "sub":
            self._ram[sp - 2] = self._ram[sp - 2] - self._ram[sp - 1]
            sp -= 1
        elif commmand == "neg":
            self._ram[sp - 1] = -self._ram[sp - 1]
        elif commmand == "eq":
            if self._ram[sp - 2] == self._ram[sp - 1]:
                self._ram[sp - 2] = -1
            else:
                self._ram[sp - 2] = 0
        elif commmand == "gt":
            if self._ram[sp - 2] > self._ram[sp - 1]:
                self._ram[sp - 2] = -1
            else:
                self._ram[sp - 2] = 0
        elif commmand == "lt":
            if self._ram[sp - 2] < self._ram[sp - 1]:
                self._ram[sp - 2] = -1
            else:
                self._ram[sp - 2] = 0
        elif commmand == "and":
            self._ram[sp - 2] = self._ram[sp - 2] & self._ram[sp - 1]
            sp -= 1
        elif commmand == "or":
            self._ram[sp - 2] = self._ram[sp - 2] | self._ram[sp - 1]
            sp -= 1
        elif commmand == "not":
            self._ram[sp - 1] = ~self._ram[sp - 1]

    def _execute_push(self, content):
        sp = self._stack_top
        self._ram[sp] = content
        sp += 1
        self._stack_top = sp

    def _execute_pop(self, segment: str, index: int):
        sp = self._stack_top
        sp -= 1
        self._stack_top = sp

    def execute(self):
        ins = self._current_instrument
        command = ins[0]

        if command == "push":
            self._execute_push(ins[1])
        elif command == "pop":
            self._execute_pop(ins[1])
        elif command in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            self._execute_arithmetic(command)

    def fetch_instrument(self):
        temp_ip = self.ip
        self._current_instrument = self._instruction_ram[temp_ip]
        temp_ip += 1
        if len(self._instruction_ram) == temp_ip:
            self._arriveEnd = True
        else:
            self.ip = temp_ip
    
    def load_code(self, codes: [str]):
        for line in codes:
            instructions = line.split()
            if instructions[0] in ["label", "function"]: 
                self._instruction_address[instructions[1], len(self._instruction_address)]
            self._instruction_ram.append(instructions)
        self._instruction_ram.append(["end"])


    def launch(self):
        self._run()

    def _run(self):
        while True:
            self.fetch_instrument()
            self.execute()
            if self._arriveEnd == True:
                break
    
    def _load(self):
        pass

if __name__ == "__main__":
    size = 10
    vm = VM(size)
    codes = ["push 1", "push 2", "add"]
    vm.load_code(codes)
    vm.launch()
    print(vm._ram)