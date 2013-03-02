class outputBuffer(): #rename outputManager?
    oBuffer = []
    def add(self, string):
        self.oBuffer.append(string)
    def output(self):
        #print(self.oBuffer)
        for string in self.oBuffer:
            print(str(string)+"\r")
        self.oBuffer = []