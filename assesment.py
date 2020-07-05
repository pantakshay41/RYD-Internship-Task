import fitz
import re
import textract
import os
import json
class Question():
	def __init__(self):
		self.question=''
		self.option1=''
		self.option2=''
		self.option3=''
		self.option4='' 
		self.answer=''
	def get_values(self,question,answer):
		self.answer=re.match(r'[\d]+[.][(]([\d\*])[)]',answer).group(1)
			
		self.option1=re.match(r'[\w\W]+[\s]*[(][1][)][\s]*([\w\W]+?)[(]',question).group(1)
		self.option2=re.match(r'[\w\W]+[\s]*[(][2][)][\s]*([\w\W]+?)[(]',question).group(1)
		self.option3=re.match(r'[\w\W]+[\s]*[(][3][)][\s]*([\w\W]+?)[(]',question).group(1)
		self.option4=re.match(r'[\w\W]+[\s]*[(][4][)][\s]*([\w\W]+?)[(]',question).group(1)
		self.question=re.match(r'[\d]+[.][\s]*([A-Z][\w\W-]+?)[(]',question).group(1)
	def __str__(self):
		return str({'Question':self.question,'Option_A':self.option1,'Option_B':self.option2,'Option_C':self.option3,'Option_D':self.option4,'Answer':self.answer})
	def __dict__(self):
		return {'Question':self.question,'Option_A':self.option1,'Option_B':self.option2,'Option_C':self.option3,'Option_D':self.option4,'Answer':self.answer}
def extract_text(input_file,output_file):
	''' Extracts text from a given PDF file and extracts questions and options from a pdf file.
		param:
			input_file: PDF file
			output_file: JSON file
		return:
			JSON file with Inputted file name'''
	extracted_data=[]
	all_questions=[]
	all_answers=[]
	doc=fitz.open(input_file)
	for page in doc:
		text=page.getText()
		text_a=text.replace(' ','')
		answers=re.findall(r'([\d]+[.][(][\d\*][)][\n0-9])',text_a)
		questions=re.findall(r'[\d]+[.][\s][A-Z][\w\W-]+?[\w][\s][(][^0-9]',text)
		questions=[question.replace('\n',' ').replace('- ','') for question in questions]
		all_questions+=questions
		all_answers+=answers
	
	all_questions=[question for question in all_questions if '(1)' in question and '(2)' in question and '(3)' in question and '(4)' in question and question.count('.')<10]
	
	i=0
	while i<len(all_questions) :
		#if re.match(r'[\d]+?[.]',all_questions[i]).group()==re.match(r'[\d]+?[.]',all_answers[j]).group(): # I had to remove this filter as I was get a very low number of questions extracted from it that too with incorrect answers due to the typos presemt in the book. If not for those typos I would have extracted all the extractable questions with answers the given solution does not contain correct answers to the question but it extracts 9366 questions and their options correctly
		question1=Question()
		question1.get_values(all_questions[i],all_answers[i])
		extracted_data.append(question1.__dict__())
		i+=1
	with open(output_file,'w',encoding='utf-8') as out_file:
		json.dump(extracted_data,out_file,indent=4)
extract_text('book.pdf','result.json')