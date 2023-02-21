import re, os, shutil

##########################################################################
# VARIABLES ##############################################################
##########################################################################

sourceFolder = "./"
#shutil.copyfile("style.css", sourceFolder + "style.css")

##########################################################################
# FUNCTIONS AND CONSTANTS ################################################
##########################################################################

metadataEnd = r"#METADATAEND#+\n"
charSplitter = r"[a-zA-Z0-9@#=\+\(\)\{\}\s+]+"
lineStarter = tuple(["#=#", "#~#"])
imageWrapper = '<span class="popupImage"><a href="$HTMLPATH$" target="_blank"><img src="$HTMLPATH$" alt=""/>⊛</a></span>'

imageDic = {}
for i in os.listdir(sourceFolder + "images/"):
	if not i.startswith("."):
		imageDic[i] = {"path": sourceFolder + "images/" + i, "htmlPath": "./images/" + i}


def processFolio(lineOfText):
	# volume
	vol = re.search(r"FolioV(\d+)", lineOfText).group(1)
	if int(vol) == 0:
		volInfo = ""
	else:
		#volInfo = "vol. %d " % int(vol)
		volInfo = "جـ %d " % int(vol)
	# folio
	#folio = re.search(r"FolioV\d+F(\d+[AB])", lineOfText).group(1).lower()
	folio = re.search(r"FolioV\d+F(\d+[AB])", lineOfText).group(1).lower().replace("a", "و").replace("b", "ظ")
	#folioInfo = volInfo + "f.%s" % folio
	folioInfo = volInfo + "صـ %s" % re.sub(r"\b0+", "", folio)

	folioInfo = "<span class='folio'>[%s]</span>" % folioInfo
	return(folioInfo)
	

def processMetadata(metadataHeader):
	print(metadataHeader)
	metadataHeader = metadataHeader.split("\n")
	metaNew = []
	for m in metadataHeader:
		if m.startswith("#META#"):
			m = m.replace("#META#", "")
			m = m.split("::")
			key = m[0].strip().replace("_", " ")
			val = m[1].strip()
			if val != "":
				if "URL" in key:
					val = '<a href="%s" target="_blank">%s</a>' % (val, val)
				#item = "<span class='key'>%s:</span> <span class='description'>%s</span><br>" % (key, val)
				item = "<span class='key'>%s:</span> <span class='description'>%s</span>" % (key, val)
				metaNew.append(item)
	meta = "\n".join(metaNew)
	return(meta)

def converter(pathToFile):
	with open(pathToFile, "r", encoding="utf8") as f1:
		data = f1.read()
		data = re.sub("@[ptd]\d+", "", data)
		data = re.sub("===", "~~~", data)
		data = re.sub(" +", " ", data)

		#input(data)

		metadata = re.split(metadataEnd, data)[0]
		metadata = processMetadata(metadata)

		text     = re.split(metadataEnd, data)[1]
		text     = re.split("\n\n+", text.strip())

		newText = []
		footnotesData = {}

		lineCounter = 0
		for t in text[0:]:
			# process text
			if t.startswith(lineStarter):
				t = t.split("\n")
				if len(t) == 2:
					#input(t)
					if t[0].startswith("#=#"):
						dipl = t[0][3:]
						edit = t[1][3:]
					else:
						dipl = t[1][3:]
						edit = t[0][3:]

					lineCounter += 1
					newLine = ["<span class='line'>|%d|</span>" % lineCounter]

					diplList = re.split(r"(%s)" % charSplitter, dipl)
					editList = re.split(r"(%s)" % charSplitter, edit)

					#diplList = re.split(r" ", dipl.strip())
					#editList = re.split(r" ", edit.strip())
					print("-"* 80)
					print(diplList)
					print(len(diplList))
					print(editList)
					print(len(editList))
					print(pathToFile)
					print("".join(editList))
					#input()

					for i in range(0, len(diplList), 2):
						#print(i)
						#print(editList[i+1])
						#print(diplList[i])
						# separator
						#print(editList[i+1])
						#input()

						if i+1 <= len(editList)-1:
							separator = editList[i+1]
						else:
							separator = ""
						
						# appending to line
						if diplList[i] != editList[i]:
							newLine.append("%s[[%s]]%s" % (editList[i], diplList[i].replace("_", " "), separator))
						else:
							newLine.append("%s%s" % (editList[i], separator))
						#input("%s :: %s" % (diplList[i], editList[i]))
					print(newLine)
					newLine = "".join(newLine)

					newText.append(newLine)

			# process folio information
			elif t.startswith("Folio"):
				#print("processing folio")
				#print(t)
				t = processFolio(t)
				newText.append(t)

			# process 
			elif t.startswith("#*#"):
				fnID   = t[3:].split("::")[0].strip()
				fnBody = t[3:].split("::")[1].strip()
				footnotesData[fnID] = "<i>comment</i>: " + fnBody

			elif t.startswith("#+#"):
				fnID   = t[3:].split("::")[0].strip()
				fnBody = t[3:].split("::")[1].strip()
				footnotesData[fnID] = "<i>insert</i>: " + fnBody

			# catch errors
			else:
				print(t)
				print("Error in encoding...")

		print(footnotesData)

		textFinal = "=====".join(newText)

		# process footnotes and comments
		footnotesFinal = []
		variants = []
		fnCounter = 0
		for k,v in footnotesData.items():
			fnCounter += 1
			#refMap = textFinal.count(k)
			refMap = len(re.findall(r"\b%s\b" % k, textFinal))
			#print(refMap)

			if refMap == 2:
				counterTemp = 0
				print(k)
				m1 = "<span class='comment'>%d{{</span>" % fnCounter
				m2 = "<span class='comment'>}}%d</span>" % fnCounter
				textFinal = re.sub(r"\b%s\b(.*)\b%s\b" % (k, k), r"%s\1%s" % (m1, m2), textFinal)

				print("\b%s (.*) %s\b" % (k, k))

				footNote = m1 + " ... " + m2 + " : " + v + "; <br>"
				footnotesFinal.append(footNote)

			elif refMap == 1:
				counterTemp = 0
				print(k)
				m1 = "<span class='fnt'>((%d))</span>" % fnCounter
				textFinal = re.sub(r"\b%s\b" % (k), r"%s" % (m1), textFinal)

				#footNote = m1 + " ... " + m2 + " : " + v + ".<br>"
				footNote = m1 + " : " + v + "; <br>"
				footnotesFinal.append(footNote)

			else:
				print(v, v)
				print("ERROR! ERROR! ERROR")

		# process variations
		#variants = []
		varCounter = 1
		#for i in re.finditer(r"\b([^\[^\b^\s]+\[\[[^\]]+\b\]\])", textFinal):
		for i in re.finditer(r"\b([^\s]+\[\[[^\]]+\]\])", textFinal):
			print(i)
			matchV = i.group(1)
			replaceV = matchV.split("[[")[0] + "<span class='fnt'>%d</span>" % varCounter
			variantFN = "<span class='fnt'>%d</span>: " % varCounter + matchV[:-2].split("[[")[1]
			variantFN = variantFN.replace("~~~", " <b><i>...</i></b>")
			textFinal = textFinal.replace(matchV, replaceV)

			print(variantFN)
			variants.append(variantFN)
			varCounter += 1

		#print(footnotesData)

		textFinal = textFinal.replace("=====", "\n")
		textFinal = "<p class='mainText'>\n\n%s\n\n</p>" % textFinal
		comments  = "<h3>Comments</h3>\n\n" + "<p class='comments'>\n\n%s\n\n</p>" % "\n".join(footnotesFinal)
		variants  = "<h3>Variants</h3>\n\n" + "<p class='variants'>\n\n%s\n\n</p>" % "\n".join(variants)
		metadata  = "<h3>Metadata</h3>\n\n" + "<p class='metadata'>\n\n%s\n\n</p>" % metadata

		textFinal = textFinal + variants + comments + metadata

		# REMOVE SOME ELEMENTS
		textFinal = textFinal.replace("BR", "")
		textFinal = textFinal.replace("INSERT_HERE", "<i>no data has been provided</i>")
		textFinal = re.sub("@[pt]\d+", "", textFinal)

		print(textFinal)

		# INSERT IMAGES
		for k,v in imageDic.items():
			find = k.split(".")[0]
			repl = imageWrapper.replace("$HTMLPATH$", v["htmlPath"])
			#print(find, " >>>> ", repl)
			#input()
			#textFinal = textFinal.replace(find, repl)
			textFinal = re.sub(r"\b%s\b" % find, repl, textFinal)

		with open("template_index.html", "r", encoding="utf8") as f1:
			template = f1.read()

		template = template.replace("@MAINCONTENT@", textFinal)

		with open(pathToFile.replace(".mARkdownMSS", ".html"), "w", encoding="utf8") as f9:
			f9.write(template)

##########################################################################
# RUNNING ################################################################
##########################################################################

files = []
for f in sorted(os.listdir(sourceFolder)):
	if f == "":
		break
	else:
		if not f.startswith(".") and f.endswith(".mARkdownMSS"):
			print("## ", f)
			converter(sourceFolder + f)

##########################################################################
# REFERENCES #############################################################
##########################################################################
# http://jsfiddle.net/4hzenxkh/1/ - CSS example of image popup (no JS)
##########################################################################