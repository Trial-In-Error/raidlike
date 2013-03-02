class outputBuffer(): #rename outputManager?
    oBuffer = []
    def add(self, string):
        self.oBuffer.append(string)
    def output(self):
        for string in self.oBuffer:
            print(string+"\r")
        self.oBuffer = []