#!/usr/bin/env python
#-*- coding:utf-8 -*-


class Table(object):
    def __init__(self,title,headers,rows):
        self.title=title
        self.headers=headers
        self.rows=rows
        self.nrows=len(self.rows)
        self.fieldlen=[]

        ncols=len(headers)

        for i in range(ncols):
            max=0
            for j in rows:
                if len(str(j[i]))>max: max=len(str(j[i]))
            self.fieldlen.append(max)

        for i in range(len(headers)):
            if len(str(headers[i]))>self.fieldlen[i]: self.fieldlen[i]=len(str(headers[i]))


        self.width=sum(self.fieldlen)+(ncols-1)*3+4

    def __str__(self):
        bar="-"*self.width
        title="| "+self.title+" "*(self.width-3-(len(self.title)))+"|"
        out=[bar,title,bar]
        header=""
        for i in range(len(self.headers)):
            header+="| %s" %(str(self.headers[i])) +" "*(self.fieldlen[i]-len(str(self.headers[i])))+" "
        header+="|"
        out.append(header)
        out.append(bar)
        for i in self.rows:
            line=""
            for j in range(len(i)):
                line+="| %s" %(str(i[j])) +" "*(self.fieldlen[j]-len(str(i[j])))+" "
            out.append(line+"|")

        out.append(bar)
        return "\r\n".join(out)