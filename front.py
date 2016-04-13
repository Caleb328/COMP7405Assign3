from Tkinter import  *
import versionOne as optFunc

class Application(Frame):

    def say_hi(self):
        print 'hi there, everyone!'

    def createInput(self):
        bottomFrame = Frame(self)
        bottomFrame.pack(side = BOTTOM)

        var = StringVar()
        lable = Label(bottomFrame, textvariable = var, relief = RAISED)
        var.set('Hi there everyone!')
        lable.pack()

    def createWidgets(self):

        topFrame = Frame(self)
        topFrame.pack(side=TOP)

        self.Q1 = Button(topFrame)
        self.Q1['text'] = "Question1",
        self.Q1["command"] = self.say_hi
        self.Q1.pack({'side':'left'})

        self.Q2 = Button(topFrame, text='Question2')
        self.Q2['command'] = self.createInput
        self.Q2.pack({'side':'left'})

        self.QUIT = Button(self, text='Quit', bg='blue')
        self.QUIT['command'] = self.quit
        self.QUIT.pack(side=TOP, anchor=E, expand=YES)



    def __init__(self, master):
        root.minsize(width = 480, height = 360)
        root.maxsize(width = 800, height = 600)
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


class Application1(Frame):

    def createWidgets(self):
        content = Frame(self)
        paramlbl = Label(content,text='Parameters',font=("Helvetica",16))
        resultlbl = Label(content, text='Results',font=("Helvetica",16))

        content.grid(column=0, row=0)
        paramlbl.grid(column=0, row=0, columnspan=5)
        resultlbl.grid(column=0, row=12, columnspan=5)

        Label(content, text = 'Calculated price is : ').grid(column=0, row=13)
        self.resultContent = Label(content, text='')
        self.resultContent.grid(column=1, row=13, columnspan = 3)

        # S1, S2, sigma1, sigma2, r, T, K, corr, type, path, cv

        lables=[
            ['spot price of asset S1', 'spot price of asset S2'],
            ['volatility of asset S1', 'volatility of asset S2'],
            ['risk-free interest rate r', 'time to maturity (in years)'],
            ['risk-free interest rate r', 'time to maturity (in years)'],

        ]
        # rows = len(lables)
        # print '-----------', rows
        # for i in range(1, rows+1, 1):
        #     print i


        self.param11lbl = Label(content, text='spot price of asset S1')
        self.param11lbl.grid(column=0, row=1)
        self.param11 = Entry(content)
        self.param11.grid(column=1, row=1, columnspan=1)

        self.param12lbl = Label(content, text='spot price of asset S2')
        self.param12lbl.grid(column=2, row=1)
        self.param12 = Entry(content)
        self.param12.grid(column=3, row=1, columnspan=1)

        self.param21lbl = Label(content, text='volatility of asset S1')
        self.param21lbl.grid(column=0, row=2, columnspan=1)
        self.param21 = Entry(content)
        self.param21.grid(column=1, row=2, columnspan=1)

        self.param22lbl = Label(content, text='volatility of asset S2')
        self.param22lbl.grid(column=2, row=2, columnspan=1)
        self.param22 = Entry(content)
        self.param22.grid(column=3, row=2, columnspan=1)

        self.param31lbl = Label(content, text='risk-free interest rate r')
        self.param31lbl.grid(column=0, row=3, columnspan=1)
        self.param31 = Entry(content)
        self.param31.grid(column=1, row=3, columnspan=1)

        self.param32lbl = Label(content, text='time to maturity(in years) T')
        self.param32lbl.grid(column=2, row=3, columnspan=1)
        self.param32 = Entry(content,text='1')
        self.param32.grid(column=3, row=3, columnspan=1)

        self.param41lbl = Label(content, text='strike price K')
        self.param41lbl.grid(column=0, row=4, columnspan=1)
        self.param41 = Entry(content)
        self.param41.grid(column=1, row=4, columnspan=1)

        self.param42lbl = Label(content, text='option type P/C')
        self.param42lbl.grid(column=2, row=4, columnspan=1)
        # self.param42 = Entry(content)
        # self.param42.grid(column=3, row=4, columnspan=1)
        self.optionType = StringVar()
        typeBtn1 = Radiobutton(content, text="call", variable=self.optionType, value="C")
        typeBtn2 = Radiobutton(content, text="put", variable=self.optionType, value="P")
        typeBtn1.grid(column=3, row=4, sticky=W)
        typeBtn2.grid(column=3, row=4, sticky=E)
        typeBtn1.invoke()



        self.param51lbl = Label(content, text='correlation p')
        self.param51lbl.grid(column=0, row=5, columnspan=1)
        self.param51 = Entry(content)
        self.param51.grid(column=1, row=5, columnspan=1)

        self.param61lbl = Label(content, text='no. of steps N')
        self.param61lbl.grid(column=0, row=6, columnspan=1)
        self.param61 = Entry(content)
        self.param61.grid(column=1, row=6, columnspan=1)

        self.param71lbl = Label(content, text='PATH')
        self.param71lbl.grid(column=0, row=7, columnspan=1)
        self.param71 = Entry(content)
        self.param71.grid(column=1, row=7, columnspan=1)

        self.param72lbl = Label(content, text='CV')
        self.param72lbl.grid(column=2, row=7, columnspan=1)
        self.param72 = Entry(content)
        self.param72.grid(column=3, row=7, columnspan=1)


        self.questionValue = StringVar()
        questionBtn1 = Radiobutton(content, text="Q1 European call/put option", variable=self.questionValue, value="Q1", command=self.selected)
        questionBtn1.grid(column=0, row=9)
        questionBtn2 = Radiobutton(content, text="Q2 Implied volatility calculator", variable=self.questionValue, value="Q2", command=self.selected)
        questionBtn2.grid(column=1, row=9)
        questionBtn3 = Radiobutton(content, text="Q3 American call/put option", variable=self.questionValue, value="Q3", command=self.selected)
        questionBtn3.grid(column=2, row=9)
        questionBtn4 = Radiobutton(content, text="Q4 GeoMetric Asian option", variable=self.questionValue, value="Q4", command=self.selected)
        questionBtn4.grid(column=0, row=10)
        questionBtn5 = Radiobutton(content, text="Q5 Arithmetic Asian option", variable=self.questionValue, value="Q5", command=self.selected)
        questionBtn5.grid(column=1, row=10)
        questionBtn6 = Radiobutton(content, text="Q6 GeoMetric basket option", variable=self.questionValue, value="Q6", command=self.selected)
        questionBtn6.grid(column=2, row=10)
        questionBtn7 = Radiobutton(content, text="Q7 Arithmetic basket option", variable=self.questionValue, value="Q7", command=self.selected)
        questionBtn7.grid(column=3, row=10)
        questionBtn1.invoke()

        calcBtn = Button(content, text='Calculate', command=self.calculate)
        quitBtn = Button(content, text='Quit', command=self.quit)
        calcBtn.grid(column=0, row=11, columnspan=2)
        quitBtn.grid(column=4, row=11, columnspan=1)

    def showResult(self,v):
        print 'result is %s' % v
        self.resultContent['text'] = v

    def calculate(self):
        # Get Parameters
        selection = self.questionValue.get()
        S1 = float(self.param11.get())
        S2 = float(self.param12.get())
        sigma1 = float(self.param21.get())
        sigma2 = float(self.param22.get())
        r = float(self.param31.get())
        T = float(self.param32.get())
        K = float(self.param41.get())
        type = self.optionType.get()
        corr = float(self.param51.get())
        n = int(self.param61.get())
        path = int(self.param71.get())
        cv = self.param72.get()

        # TODO: repo rate
        repo = 0.3
        trueValue = 10.0

        print 'TO DO-------execute calculation'
        resultPrice = 0.0000
        if selection == 'Q1':
            if type == "C":
                #stock, strike, time, maturity, volatility, repo, rfr
                return optFunc.call_black_scholes(S1, K, 0.0, T, sigma1, repo, r)
            elif type == "P":
                return optFunc.put_black_scholes(S1, K, 0.0, T, sigma1, repo, r)
            else:
                return 0.0
            # Q1
        elif selection == 'Q2':
            if type == 'C':
                #S, K, t, T, q, r, pTrue
                return optFunc.implied_vol_C(S1, K, 0.0, T, repo, r, trueValue)
            elif type == 'P':
                return optFunc.implied_vol_P(S1, K, 0.0, T, repo, r, trueValue)
            else:
                return 0.0
            # Q2
        elif selection == 'Q3':
            #S, K, r, T, sigma, N, type
            return optFunc.bino_tree(S1, K, r, T, sigma1, n, type)
            # Q3
        elif selection == 'Q4':
            #S, sigma, r, t, K, n, type
            return optFunc.geo_asian_option(S1, sigma1, r, 0.0, K, n, type)
            # Q4
        elif selection == 'Q5':
            #S, sigma, r, T, K, step, type, path, cv
            resultPrice = optFunc.arith_asian_option(S1, sigma1, r, T, K, n, type, path, cv)
            # Q5
        elif selection == 'Q6':
            #S1, S2, sigma1, sigma2, r, T, K ,corr, type
            return optFunc.geo_basket(S1, S2, sigma1, sigma2, r, T, K ,corr, type)
            # Q6
        elif selection == 'Q7':
            #S1, S2, sigma1, sigma2, r, T, K, corr, type, path, cv
            return optFunc.arith_basket(S1, S2, sigma1, sigma2, r, T, K, corr, type, path, cv)
            # Q7
        self.resultContent['text'] = "%.5f" % resultPrice


    def selected(self):
        selection = self.questionValue.get()
        # print "qusetion", selection
        if selection=='Q1':
            self.param12lbl.grid_forget()
            self.param12.grid_forget()
            self.param22lbl.grid_forget()
            self.param22.grid_forget()
            print "TO DO-----qusetion", selection
            # Q1
        elif selection=='Q2':
            self.param12lbl.grid_forget()
            self.param12.grid_forget()
            self.param22lbl.grid_forget()
            self.param22.grid_forget()
            print "TO DO-----qusetion", selection
            # Q2
        elif selection=='Q3':
            self.param12lbl.grid_forget()
            self.param12.grid_forget()
            self.param22lbl.grid_forget()
            self.param22.grid_forget()
            print 'TO DO-----question'% selection
        elif selection=='Q4':
            self.param12lbl.grid_forget()
            self.param12.grid_forget()
            self.param22lbl.grid_forget()
            self.param22.grid_forget()
            print "TO DO-----qusetion", selection
            # Q4
        elif selection=='Q5':
            self.param12lbl.grid_forget()
            self.param12.grid_forget()
            self.param22lbl.grid_forget()
            self.param22.grid_forget()
            print "TO DO-----qusetion", selection
            # Q5
        elif selection=='Q6':
            self.param12lbl.grid(column=2, row=1)
            self.param12.grid(column=3, row=1, columnspan=1)
            self.param22lbl.grid(column=2, row=2, columnspan=1)
            self.param22.grid(column=3, row=2, columnspan=1)
            print "TO DO-----qusetion", selection
            # Q6
        elif selection=='Q7':
            self.param12lbl.grid(column=2, row=1)
            self.param12.grid(column=3, row=1, columnspan=1)
            self.param22lbl.grid(column=2, row=2, columnspan=1)
            self.param22.grid(column=3, row=2, columnspan=1)
            print "TO DO-----qusetion", selection
            # Q7


    def __init__(self, master):
        root.minsize(width = 960, height = 400)
        root.maxsize(width = 1440, height = 600)
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
app = Application1(master=root)
app.mainloop()
root.destroy()



"""
            self.param12lbl.grid_forget()
            self.param12.grid_forget()
            self.param22lbl.grid_forget()
            self.param22.grid_forget()

            # self.param11lbl = Label(content, text='spot price of asset S1')
            self.param11lbl.grid(column=0, row=1)
            self.param11.grid(column=1, row=1, columnspan=1)

            # self.param12lbl = Label(content, text='spot price of asset S2')
            self.param12lbl.grid(column=2, row=1)
            self.param12.grid(column=3, row=1, columnspan=1)

            # self.param21lbl = Label(content, text='volatility of asset S1')
            self.param21lbl.grid(column=0, row=2, columnspan=1)
            self.param21.grid(column=1, row=2, columnspan=1)

            # self.param22lbl = Label(content, text='volatility of asset S2')
            self.param22lbl.grid(column=2, row=2, columnspan=1)
            self.param22.grid(column=3, row=2, columnspan=1)

            # self.param31lbl = Label(content, text='risk-free interest rate r')
            self.param31lbl.grid(column=0, row=3, columnspan=1)
            self.param31.grid(column=1, row=3, columnspan=1)

            # self.param32lbl = Label(content, text='time to maturity(in years) T')
            self.param32lbl.grid(column=2, row=3, columnspan=1)
            self.param32.grid(column=3, row=3, columnspan=1)

            # self.param41lbl = Label(content, text='strike price K')
            self.param41lbl.grid(column=0, row=4, columnspan=1)
            self.param41.grid(column=1, row=4, columnspan=1)

            # self.param42lbl = Label(content, text='option type P/C')
            self.param42lbl.grid(column=2, row=4, columnspan=1)
            self.param42.grid(column=3, row=4, columnspan=1)

            # self.param51lbl = Label(content, text='correlation p')
            self.param51lbl.grid(column=0, row=5, columnspan=1)
            self.param51.grid(column=1, row=5, columnspan=1)

            # self.param61lbl = Label(content, text='no. of steps N')
            self.param61lbl.grid(column=0, row=6, columnspan=1)
            self.param61.grid(column=1, row=6, columnspan=1)

            # self.param71lbl = Label(content, text='PATH')
            self.param71lbl.grid(column=0, row=7, columnspan=1)
            self.param71.grid(column=1, row=7, columnspan=1)

            # self.param72lbl = Label(content, text='CV')
            self.param72lbl.grid(column=2, row=7, columnspan=1)
            self.param72.grid(column=3, row=7, columnspan=1)
"""