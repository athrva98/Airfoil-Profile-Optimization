##### Do not change any Part of this Code #####

class Bezier_Curve_generator:
    
    
    temp1   = []
    generator_order = 1
    temp2    = []
    binomial = []
    def __init__(self, order_):
        self.generator_order=order_
        self.binomial = [0]* self.generator_order
        self.temp2    = [0]* self.generator_order
        self.temp1   = [0]* self.generator_order
        self.binomial[0]=1
        for i in range (1,self.generator_order+1):
            temp=self.binomial[0]
            for ii in range (1,i):
                temp2= self.binomial[ii]
                self.binomial[ii]=temp+self.binomial[ii]
                temp = temp2
     

    def curve_interpolation(self,coefficients, number ):
        output = [0]*(number+1)
        step = 1.0/float(number)
        temp3 = 0
        output[0]=coefficients[0]
        for i in range (1,number+1):
            temp3+=step
            temp4=1.0-temp3
            temp5=1.0
            temp7=1.0
            for j in range (0,self.generator_order):  # generate powers of temp3
                self.temp2[j] = temp5;
                self.temp1[self.generator_order-j-1] = temp7
                temp5*=temp3
                temp7*=temp4
            output[i]=0
            for j in range (0,self.generator_order):  
                output[i]+=coefficients[j]*self.temp1[j]*self.temp2[j]*self.binomial[j]
        return output


