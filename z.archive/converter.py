import re, os

folderSRC = "./sent/"
folderTRG = "./converted/"


def converter(folderSRC, folderTRG):
	files = os.listdir(folderSRC)

	for f in files:
		path1 = os.path.join(folderSRC, f)

		with open(path1, "r", encoding="utf8") as f1:
			data = f1.read()
			data = data.replace("######OpenITI_MSS#", "#OpenITI##########################################")
			data = data.replace("#META#Header#End#",  "#METADATAEND######################################")
			data = data.replace("\t", " ")

			data = data.replace("\n#-#", "\n#=#").replace("\n#^#", "\n#~#")
			data = re.sub(r"\n(#2#)([^\n]+\n)", r"\n\1\2#3#\2", data)


			uri = re.search(r"DOCUMENT_URI([^\n]+)", data).group(1).replace(":", "").strip()

			print(uri)

			path2 = os.path.join(folderTRG, uri)



			data = re.sub(" +", " ", data)
			splitter = "### | EXAMPLES TO PASTE INTO COLLATEX - https://collatex.net/demo/"
			data = data.split(splitter)[0]
			with open(path2, "w", encoding="utf8") as f9:
				f9.write(data)


converter(folderSRC, folderTRG)
