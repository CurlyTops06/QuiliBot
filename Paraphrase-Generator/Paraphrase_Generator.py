from cgitb import enable
from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer
from nltk import pos_tag
from nltk.corpus import wordnet
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.error import HTTPError
from random_word import RandomWords
import nltk 
from threading import Thread
from pattern.en import superlative,pluralize,comparative,superlative
import spacy
from tkinter import filedialog
import csv
import ast
import requests
import os
import random 
from pyinflect import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import tkinter.font as tkFont
import tkinter as tk
import tkinter.ttk as ttk
import random
import Functions as fn
from fix_grammar import Fix_Grammar
from paraphrase import Paraphraser
import torch
import warnings
import re
quotes_list=['“ Trees that are slow to grow bear the best fruit. ”\n\n      ― Moliere','“ He that can have patience can have what he will. ”\n \n      ― Benjamin Franklin','“ Patience is a conquering virtue. ” \n\n        ― Geoffrey Chaucer','“ Patience is bitter, but its fruit is sweet. ”\n\n        ― Aristotle','“ The strongest of all warriors are these two — Time and Patience. ” \n\n         ― Leo Tolstoy, War and Peace','“ Rivers know this: there is no hurry. We shall get there some day. ”\n\n           ― A.A. Milne, Winnie-the-Pooh']

#root=Tk() #main GUI window

##model which contains word vectors (used in program to compare similarities)
#root.wm_title('Paraphrase Generator')
#spacy.cli.download("en_core_web_lg")
nlp = spacy.load('en_core_web_lg')
#file containing input

class App:
    def __init__(self, root):
        #setting title
        root.title("QuiliBot - Paraphraser")
        #icon
        root.iconbitmap('.img\\icons8-bot-80.ico')
        #setting window size
        width=1312
        height=625
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        def set_seed(seed):
          torch.manual_seed(seed)
          if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

        def progressbar(i):
            label['text']=str(i+1)+'/'+str(total_length)
            bar['value']=(100/total_length)*(i+1)
            status.config(text=words[i])
            quote['text']=quotes_list[random.randint(0,len(quotes_list)-1)]
            if i+1==total_length:
                top.destroy()

        #1st function to find similarities
        def synonyms2(term):
            synonyms_ = [] 
            for syn in wordnet.synsets(term): 
                for l in syn.lemmas(): 
                    synonyms_.append(l.name()) 
        
            return synonyms_

        def synonyms(string):
 
            try:
                if string!=u'"' and string!=u'\"' and string!=u'\'' and string!=u"'":
                    stripped_string = string.strip()
                    fixed_string = stripped_string.replace(" ", "_")
   
                # Set the url using the amended string
                    my_url = f'https://thesaurus.plus/thesaurus/{fixed_string}'
                # Open and read the HTMLz
                    uClient = uReq(my_url)
                    page_html = uClient.read()
                    uClient.close()
                # Parse the html into text
                    page_soup = soup(page_html, "html.parser")
                    word_boxes = page_soup.find("ul", {"class": "list paper"})
                    results = word_boxes.find_all("div", "list_item")
                    sim_words_list=[]
               # Iterate over results and print
                    for result in results:
                        sim_words_list.append(result.text)
                # Remove whitespace before and after word and use underscore between words
        
            except Exception as e:
                sim_words_list=[]
        
                if "_" in fixed_string:
                    print(e)

                else:
                    print(e)
            print('yeahh')
            return sim_words_list
        def syn(word):
            urls=["https://dictionaryapi.com/api/v3/references/thesaurus/json/{}?key=a24dfaa9-ffe0-4a9a-8906-c8ff3e8dd406".format(word),"https://dictionaryapi.com/api/v3/references/thesaurus/json/{}?key=92432adb-24d2-46a1-a979-f1b701155bf2".format(word)]
            return_list=[]
            try:
                url=urls[random.randint(0,1)]
                r = requests.get(url)
        
                if r.json()!=[] or  r.json()!='':
                    return_list=r.json()[0]['meta']['syns'][0]
            
                else:
                    raise Exception('error')
                print('1')
            except:
                try:
                    url=urls[random.randint(0,1)]
                    r = requests.get(url)
                    if r.json()!=[] or  r.json()!='':
                        return_list=r.json()[0]['meta']['syns'][0]
                    else:
                        return_list=r.json()[0]['meta']['syns'][0]
                        raise Exception('error')
                    print('2')
                except:
                    try:
                        url = "https://dictionaryapi.com/api/v3/references/ithesaurus/json/{}?key=61d0a7b2-125f-4b16-b0d8-1f3593627bf9".format(word)
                        r = requests.get(url)
                        if r.json()!=[] or  r.json()!='':
                            return_list=r.json()[0]['meta']['syns'][0]
                        else:
                            return_list=r.json()[0]['meta']['syns'][0]
                            raise Exception('error')
                        print('3')
                    except:
                        try:
                            url = "https://dictionaryapi.com/api/v3/references/ithesaurus/json/{}?key=ea94eb40-67b0-4a3d-ba53-5a3da9079906".format(word)
                   
                            r = requests.get(url)
                            if r.json()!=[] or  r.json()!='':
                                return_list=r.json()[0]['meta']['syns'][0]
                            print('4')
                        except:
                            if  word not in ['.',',','(' ,')','',' (','( ',' )',') ',' .','. ','!','doesn','t','don','\'','i','l',' t','t ','\'t', "'",'wasn','didn','couldn','wouldn','weren',';',':','|','I','l','L','s','ain','shouldn','&','?',"\'","'",'"','\"']:
                                if word!='\"' and word!='"' and word!='\'' and word!="'":

                                    return_list=[]
                            else:
                                return_list=[]

            if return_list!=[]:
                with open('.img\\words.csv','a',newline='') as csvfile:
                    wr=csv.writer(csvfile)
                    global d
                    d={'id':word,'value':return_list}
                    for i in range(int(len(d)/2)):
                        k=tuple(d.values())
                        w=k[0]
                        v=k[1]
                        wr.writerow([w,v])
            return return_list

        def fun(word):
            csv__file= open('.img\\words.csv','r') 
            reader=csv.reader(csv__file)
            k=True
            if reader!=[]:
                for row in reader:
            
                    if row!=[]:
                        if row[0].lower()==word.lower():
                            k=False
                    
                            return (ast.literal_eval(row[1]))

                        else:
                            k=True
                    
                if k==True:
                    return (syn(word))
        def start(position=None,*args):
    
            global output,output2,total_length,words

            gf = Fix_Grammar(models = 1, use_gpu=False) # 1=corrector, 2=detector

            fixed_spell = fn.fix_spelling(input_box.get('1.0','end-1c')) #fixes spelling

            set_seed(1212) #fixes grammar
            fixed_grammar = gf.correct(fixed_spell, max_candidates=1)

            warnings.filterwarnings("ignore")
            set_seed(1234)
            paraphrase = Paraphraser(model_tag="prithivida/parrot_paraphraser_on_T5")
            sentence_tokenize = sent_tokenize(fixed_grammar)
            for sentence in sentence_tokenize:
                para_phrases = paraphrase.rephrase(input_phrase=sentence, use_gpu=False)
                result_box1.insert(END,". ")
                for para_phrase in para_phrases:
                    result_box1.insert(END,para_phrase)

            tokenizer=RegexpTokenizer(r'\s+', gaps=True)
            words=tokenizer.tokenize(result_box1.get('1.0','end-1c'))
            total_length=len(words)
            taggs=pos_tag(words)
            output=''
            output2=''

            real_words=[]
            for i in range(len(words)):
                a=taggs[i][1]
                print('word: ',words[i] ,'tag: ',a)
                r=[]
                # not to fin synonym for the name of a person,a decorator etc.
                if ( taggs[i][1]!='DP' and taggs[i][1]!='CD' and taggs[i][1]!='TO' and taggs[i][1]!='PRP$' and taggs[i][1]!='IN' and taggs[i][1]!='PRP'  and taggs[i][1]!='DT'  and taggs[i][1]!='WRB' and   taggs[i][1]!='WR') and( words[i] not in ['.',',','(' ,')','',' (','( ',' )',') ',' .','. ','!','doesn','t','don','\'','i','l',' t','t ','\'t', "'",'wasn','didn','couldn','wouldn','weren','I','L','1','|',';',':','s',' s','ain','ll','-','__']) and words[i].lower() not in ['time','second','seconds','month','months','year','years','minute','minutes','indian','countries','let']:
                    if words[i]!='.' and words[i]!=',' and words[i]!="'" and words[i]!="\"" and words[i]!="\"" and words[i]!='"' and words[i]!=' "' and words[i]!='" ' and words[i]!='?':
                        r=fun(words[i])
        
                progressbar(i)
                
                if r!=[]:
                    print('list of words: ',r)
                    real_words=[]
                    # to make the similar words more similar by changing their tense etc.
                    for j in r:
                        tag=pos_tag([j])[0][1]
                        if tag==a or a=='JJ':  
                                       # if already similar
                            real_words.append(j) 
                        elif tag!=a:           #check part-of speech tags and change accordingly
                            if a=='NNPS':
                                token=nlp(j)
                                w=tokens[0]._.inflect('NNPS', form_num=0)
                                if w!=None and pos_tag([w])==a:
                                    real_words.append(tokens[0]._.inflect('NNPS',inflect_oov=True, form_num=0))
                            elif a=='NNS':
                                token=nlp(j)
                                w=token[0]._.inflect('NNS',inflect_oov=True, form_num=0)
                                if w!=None and pos_tag([w])==a:
                                    real_words.append(token[0]._.inflect('NNS',inflect_oov=True,form_num=0))
                            elif a=='NNP':
                                token=nlp(j)
                                w=token[0]._.inflect('NNP',inflect_oov=True, form_num=0)
                                if w!=None and pos_tag([w])==a:
                                    real_words.append(token[0]._.inflect('NNP',inflect_oov=True,from_num=0))
                            elif a=='NN':
                                token=nlp(j)
                                w=token[0]._.inflect('NN',form_num=0)
                                real_words.append(w)
                            elif a=='RB':
                                token=nlp(j)
                                w=token[0]._.inflect('RB',inflect_oov=True,form_num=0)
                                real_words.append(token[0]._.inflect("RB",inflect_oov=True,form_num=0))
                            elif a=='RBR':
                                token=nlp(j)
                                w=token[0]._.inflect('RBR', inflect_oov=True,form_num=0)
                                if w!=None and pos_tag([w])==a:
                                    real_words.append(token[0]._.inflect('RBR',inflect_oov=True,form_num=0))
                            elif a=='RBS':
                                token=nlp(j)
                                w=token[0]._.inflect('RBS',inflect_oov=True, form_num=0)
                                if w!=None and pos_tag([w])==a:
                                    real_words.append(token[0]._.inflect('RBS',inflect_oov=True,form_num=0))
                            elif a=='VB' :
                                tokens = nlp(j)
                                w=tokens[0]._.inflect('VB',inflect_oov=True, form_num=0)
                                if w!=None :
                                    real_words.append(tokens[0]._.inflect('VB',inflect_oov=True, form_num=0))
                            elif a=='VBD' :
                                tokens = nlp(j)
                                w=tokens[0]._.inflect('VBD', form_num=1)
                                if w!=None :
                                    real_words.append(tokens[0]._.inflect('VBD', inflect_oov=True,form_num=0))
                            elif a=='VBG':
                                tokens=nlp(j)
                                w=tokens[0]._.inflect('VBG',inflect_oov=True, form_num=0)
                                if w!=None and pos_tag([w])==a:
                                    real_words.append(tokens[0]._.inflect('VBG',inflect_oov=True, form_num=0))
                            elif a=='VBN ':
                                tokens=nlp(j)
                                w=tokens[0]._.inflect('VBN',inflect_oov=True, form_num=0)
                                if w!=None and pos_tag([w])==a:
                                    real_words.append(tokens[0]._.inflect('VBN', inflect_oov=True,form_num=0))
                            elif a=='VBP':
                                tokens=nlp(j)
                                w=tokens[0]._.inflect('VBP',inflect_oov=True, form_num=0)
                                if w!=None and pos_tag([w])==a:
                                    real_words.append(tokens[0]._.inflect('VBP',inflect_oov=True, form_num=0))
                            elif a=='VBZ':
                                tokens=nlp(j)
                                w=tokens[0]._.inflect('VBZ',inflect_oov=True, form_num=0)
                                if w!=None and pos_tag([w])==a:
                                    real_words.append(tokens[0]._.inflect('VBZ',inflect_oov=True, form_num=0))
                            elif a=='JJR' :
                                real_words.append(comparative(j))
                            elif a=='JJS' :
                                real_words.append(superlative(j))
                print('real words: ',real_words)        
                if real_words==[] or r==[]:         #if no similar word is found 
                    output=output+' '+words[i]
                    output2=output2+' '+words[i]
                else :
                    output_words=[]
                    max_sim=[]
                    token1=nlp(words[i])
                    for h in real_words:
                        if h!=None and h!='' :
                            token2=nlp(h)
                            f1=h.replace(' ','')
                            f=f1.replace('_',' ')
                            sim=token1.similarity(token2)
                            if  h not in  output_words and (f not in output_words ) and words[i].lower()!=h.lower() and  words[i].lower()!=f.lower()  :   #adding appropriate word
                                output_words.append(f)
                                max_sim.append(sim)
                        else:
                            sim=0
                    final_listwords=[]
                    for jj in max_sim:
                        final_listwords.append(output_words[max_sim.index(max(max_sim))])
                        max_sim[max_sim.index(max(max_sim))]=-1
                    if output_words==[]:
                        output=output+' '+words[i]
                        output2=output2+' '+words[i]
                    elif position==None or type(position)!=int:
                        print('final_listwords: ',final_listwords)
                        if len(output_words)>3:
                            output=output+' '+final_listwords[0]  
                        else:
                            output=output+' '+final_listwords[random.randint(0,len(final_listwords)-1)] 
                    elif position!=None and (type(position)==int or type(position)==str): 
                        if type(position)==str:                                  #choose a specific position of word from list of similar words
                            if len(output_words)>int(position)  :
                                output=output+' '+final_listwords[int(position)]
                        elif type(position)==int:
                            if len(output_words)>(position):
                                output=output+' '+final_listwords[position]
                        else:
                            output=output+' '+final_listwords[len(output_words)-1]
                    if len(output_words)>7:
                            output2=output2+' '+str([words[i]]+final_listwords[0:8])
                             # if number of similar words is less than 4 than choose randomly
                    elif len(output_words)<=7:
                            output2=output2+' '+str([words[i]]+final_listwords[0:])

            word_count2.config(text=f"    Words: {total_length}")
            result_box2.insert(END,output2)

        def go_(): 
            if input_box.get('1.0','end-1c')=='' or input_box.get('1.0','end-1c')==' ':
                messagebox.showinfo('QuiliBot - Invalid!','Insert Text First!')
                result_box1.delete('1.0',END)
                result_box2.delete('1.0',END)
                result_box2.insert(END,'NOTHING TO PROCESS IN INPUTBOX !!!')
                result_box1.insert(END,'NOTHING TO PROCESS IN INPUTBOX !!!')
            else:
                global bar,label,top,quote,status
                top=Toplevel(root,bg='white')
                top.title('QuiliBot - In Progress...') 
                top.geometry('500x300')
                top.iconbitmap('.img\\icons8-bot-80.ico')
                style = ttk.Style()
                style.theme_use('vista')
                style.configure("black.Horizontal.TProgressbar", background='blue',bg="white",fg="black")
                bar = Progressbar(top, length=200, style='black.Horizontal.TProgressbar')
                bar['value'] = 0
                bar.place(relx=0.3,rely=0.07)
                status=Label(top,bg="white",fg="black")
                status.place(relx=0.13,rely=0.07)

                label=Label(top,bg="white",fg="black")
                label.place(relx=0.45,rely=0.2)
                quote=Label(top,font=('Arial',12),text=quotes_list[random.randint(0,len(quotes_list)-1)],bg="white",fg="black",justify=CENTER,anchor=CENTER)
                quote.place(relwidth=1,relx=0,rely=0.4,relheight=0.6)
                result_box2.delete('1.0',END)
                result_box1.delete('1.0',END)
                if pos.get()==-1:
                    Thread(target=start).start()
                else:
                    Thread(target=start,args=(pos.get(),)).start()
                    pos.set(-1)
            
        def exit_():  #exit
            ms = messagebox.askquestion('QuiliBot - Exiting...', 'Are You Sure?')
            if ms == 'yes':
                root.destroy()

        def clear_(): #to clear screen
            ms = messagebox.askquestion('QuiliBot - Clear Inputs?', 'Are You Sure?')
            if ms == 'yes':
                input_box.delete('1.0',END)
                result_box1.delete('1.0',END)
                result_box2.delete('1.0',END)
                word_count1.config(text="    Words:")
                word_count2.config(text="    Words:")
            
 ########################################################################### GUI     

        GLabel_246=tk.Label(root)
        ft = tkFont.Font(family='Times',size=23)
        GLabel_246["font"] = ft
        GLabel_246["fg"] = "#00008B"
        GLabel_246["justify"] = "center"
        GLabel_246["text"] = "Bot"
        GLabel_246.place(x=103,y=10,width=84,height=41)

        GLabel_992=tk.Label(root)
        ft = tkFont.Font(family='Times',size=23)
        GLabel_992["font"] = ft
        GLabel_992["fg"] = "#0000ff"
        GLabel_992["justify"] = "center"
        GLabel_992["text"] = "Quili"
        GLabel_992.place(x=60,y=10,width=62,height=41)


        GLabel_325=tk.Label(root)
        ft = tkFont.Font(family='Times',size=22)
        GLabel_325["font"] = ft
        GLabel_325["fg"] = "#333333"
        GLabel_325["justify"] = "center"
        GLabel_325["text"] = "Paraphrasing Tool"
        GLabel_325.place(x=550,y=20,width=221,height=31)
        
        def keyPress(e): #for word count
            words = input_box.get(1.0, END)
            wordcount = len( re .findall( '\w+', words ) )
            word_count1.config(text = f'    Words: {wordcount}')

        input_box=tk.Text(root, wrap=WORD)
        input_box["bg"] = "#ffffff"
        input_box["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        input_box["font"] = ft
        input_box["fg"] = "#333333"
        input_box.bind("<Key>", keyPress)
        input_box.place(x=10,y=90,width=641,height=261)

        result_box1=tk.Text(root, wrap=WORD)
        result_box1["bg"] = "#ffffff"
        result_box1["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        result_box1["font"] = ft
        result_box1["fg"] = "#333333"
        result_box1.insert(END,'#'*10+' R E S U L T '+'#'*10)
        result_box1.place(x=660,y=90,width=641,height=261)

        result_box2=tk.Text(root, wrap=WORD)
        result_box2["bg"] = "#ffffff"
        result_box2["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        result_box2["font"] = ft
        result_box2["fg"] = "#333333"
        result_box2.place(x=10,y=460,width=1291,height=136)
        
        button_start=Button(root)
        button_start["bg"] = "#00008B"
        button_start["borderwidth"] = "0px"
        ft = tkFont.Font(family='Times',size=23)
        button_start["font"] = ft
        button_start["fg"] = "#ffffff"
        button_start["justify"] = "center"
        button_start["text"] = "Rephrase"
        button_start.place(x=510,y=380,width=291,height=41)
        button_start["command"] = go_

        GLabel_365=tk.Label(root, borderwidth=2, relief="groove", anchor="w")
        GLabel_365["bg"] = "#ffffff"
        GLabel_365["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLabel_365["font"] = ft
        GLabel_365["fg"] = "#333333"
        GLabel_365["justify"] = "left"
        GLabel_365["text"] = "Paraphrased Text"
        GLabel_365.place(x=660,y=60,width=641,height=31)

        GLabel_608=tk.Label(root, borderwidth=2, relief="groove", anchor="w")
        GLabel_608["bg"] = "#ffffff"
        GLabel_608["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLabel_608["font"] = ft
        GLabel_608["fg"] = "#333333"
        GLabel_608["justify"] = "left"
        GLabel_608["text"] = "Standard Paraphrase"
        GLabel_608.place(x=10,y=60,width=641,height=31)

        GLabel_427=tk.Label(root, borderwidth=2, relief="groove", anchor="w")
        GLabel_427["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=14)
        GLabel_427["font"] = ft
        GLabel_427["fg"] = "#333333"
        GLabel_427["justify"] = "left"
        GLabel_427["text"] = "Synonyms"
        GLabel_427.place(x=10,y=430,width=1291,height=31)
            
        word_count1=tk.Label(root, borderwidth=2, relief="groove", anchor="w")
        word_count1["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=12)
        word_count1["font"] = ft
        word_count1["fg"] = "#333333"
        word_count1["justify"] = "left"
        word_count1["text"] = "    Words:"
        word_count1.place(x=10,y=350,width=641,height=21)

        word_count2=tk.Label(root, borderwidth=2, relief="groove", anchor="w")
        word_count2["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=12)
        word_count2["font"] = ft
        word_count2["fg"] = "#333333"
        word_count2["justify"] = "left"
        word_count2["text"] = "    Words:"
        word_count2.place(x=660,y=350,width=641,height=21)

        menu1 = Menu(root, bg='red', fg='blue', activeforeground='#209EFF', font=('Areial', 10))
        sub1 = Menu(menu1, tearoff=0, activebackground='white', activeforeground='#209EFF', bg='white', )
        menu1.add_command(label='CLEAR ', command=clear_,)
        menu1.add_command(label='EXIT', command=exit_, )

        root.config(menu=menu1)

        pos=IntVar()
        pos.set(-1)
        
if __name__ == "__main__":
    root = tk.Tk()
    img=PhotoImage(file=".img\\rsz_icons8-bot-80.png")
    GLabel_671=tk.Label(image=img)
    GLabel_671.pack()
    GLabel_671.place(x=10,y=10,width=41,height=41)
    app = App(root)
    root.mainloop()