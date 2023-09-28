import re, os, shutil
from bs4 import BeautifulSoup

##########################################################################
# VARIABLES ##############################################################
##########################################################################

sourceFolder = ""
# shutil.copyfile("style.css", sourceFolder + "style.css")

##########################################################################
# FUNCTIONS AND CONSTANTS ################################################
##########################################################################

metadataEnd = r"#METADATAEND#+\n"
charSplitter = r"[a-zA-Z0-9@#=\+\(\)\{\}\s+]+"
lineStarter = tuple(["#=#", "#~#"])
lineStarterMargin = tuple(["#==#", "#~~#"])
imageWrapper = '<span class="popupImage"><a href="$HTMLPATH$" target="_blank"><img src="$HTMLPATH$" alt=""/>⊛</a></span>'

imageDic = {}
for i in os.listdir(sourceFolder + "images/"):
    if not i.startswith("."):
        imageDic[i] = {
            "path": sourceFolder + "images/" + i,
            "htmlPath": "./images/" + i,
        }


def intToRoman(num):
    m = ["", "M", "MM", "MMM"]
    c = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]

    ans = thousands + hundreds + tens + ones

    return ans


def processFolio(lineOfText):
    # volume
    vol = re.search(r"FolioV(\d+)", lineOfText).group(1)
    if int(vol) == 0:
        volInfo = ""
    else:
        # volInfo = "vol. %d " % int(vol)
        volInfo = "جـ %d " % int(vol)
    # folio
    # folio = re.search(r"FolioV\d+F(\d+[AB])", lineOfText).group(1).lower()
    folio = (
        re.search(r"FolioV\d+F(\d+[AB])", lineOfText)
        .group(1)
        .lower()
        .replace("a", "و")
        .replace("b", "ظ")
    )
    # folioInfo = volInfo + "f.%s" % folio
    folioInfo = volInfo + "صـ %s" % re.sub(r"\b0+", "", folio)

    folioInfo = "<span class='folio'>[%s]</span>" % folioInfo
    return folioInfo


def processPage(lineOfText):
    # volume
    vol = re.search(r"PageV(\d+)", lineOfText).group(1)
    if int(vol) == 0:
        volInfo = ""
    else:
        # volInfo = "vol. %d " % int(vol)
        volInfo = "جـ %d " % int(vol)
    # page
    # page = re.search(r"PageV\d+P(\d+[AB])", lineOfText).group(1).lower()
    page = re.search(r"PageV\d+P", lineOfText).group(0)
    page = lineOfText.replace(page, "")
    # pageInfo = volInfo + "f.%s" % page
    pageInfo = volInfo + "صـ %s" % re.sub(r"\b0+", "", page)

    pageInfo = "<span class='folio'>[%s]</span>" % pageInfo
    return pageInfo


def processMetadata(metadataHeader):
    # print(metadataHeader)
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
                # item = "<span class='key'>%s:</span> <span class='description'>%s</span><br>" % (key, val)
                item = (
                    "<span class='key'>%s:</span> <span class='description'>%s</span>"
                    % (key, val)
                )
                metaNew.append(item)
    meta = "\n".join(metaNew)
    return meta


def converter(pathToFile):
    with open(pathToFile, "r", encoding="utf8") as f1:
        data = f1.read()
        data = re.sub("@[ptd]\d+", "", data)
        data = re.sub("===", "~~~", data)
        data = re.sub(" +", " ", data)

        # input(data)

        metadata = re.split(metadataEnd, data)[0]
        metadata = processMetadata(metadata)

        text = re.split(metadataEnd, data)[1]
        text = re.split("\n\n+", text.strip())

        newText = []
        footnotesData = {}
        insertionsData = {}
        marginalInsertionsData = {}

        editedText = ""

        lineCounter = 0
        for t in text[0:]:
            # process text
            if t.startswith(lineStarter):
                t = t.split("\n")
                if len(t) == 2:
                    # input(t)
                    if t[0].startswith("#=#"):
                        dipl = t[0][3:]
                        edit = t[1][3:]
                    else:
                        dipl = t[1][3:]
                        edit = t[0][3:]

                    editedText += edit

                    lineCounter += 1
                    newLine = ["<span class='line'>|%d|</span>" % lineCounter]

                    diplList = re.split(r"(%s)" % charSplitter, dipl)
                    editList = re.split(r"(%s)" % charSplitter, edit)

                    # diplList = re.split(r" ", dipl.strip())
                    # editList = re.split(r" ", edit.strip())
                    # print("-" * 80)
                    # print(diplList)
                    # print(len(diplList))
                    # print(editList)
                    # print(len(editList))
                    # print(pathToFile)
                    # print("".join(editList))
                    # input()

                    for i in range(0, len(diplList), 2):
                        # print(i)
                        # print(editList[i+1])
                        # print(diplList[i])
                        # separator
                        # print(editList[i+1])
                        # input()

                        if i + 1 <= len(editList) - 1:
                            separator = editList[i + 1]
                        else:
                            separator = ""

                        # appending to line
                        if diplList[i] != editList[i]:
                            newLine.append(
                                "%s[[%s]]%s"
                                % (
                                    editList[i],
                                    diplList[i].replace("_", " "),
                                    separator,
                                )
                            )
                        else:
                            newLine.append("%s%s" % (editList[i], separator))
                        # input("%s :: %s" % (diplList[i], editList[i]))
                    # print(newLine)
                    newLine = "".join(newLine)

                    newText.append(newLine)

            elif t.startswith(lineStarterMargin):
                t = t.split("\n")
                if len(t) == 2:
                    # input(t)
                    if t[0].startswith("#==#"):
                        dipl = t[0][4:]
                        edit = t[1][4:]
                    else:
                        dipl = t[1][4:]
                        edit = t[0][4:]

                    editedText += edit

                    lineCounter += 1
                    newLine = []

                    diplList = re.split(r"(%s)" % charSplitter, dipl)
                    editList = re.split(r"(%s)" % charSplitter, edit)

                    # print(diplList, editList)

                    for i in range(0, len(diplList), 2):
                        if i + 1 <= len(editList) - 1:
                            separator = editList[i + 1]
                        else:
                            separator = ""

                        # appending to line
                        if diplList[i] != editList[i]:
                            newLine.append(
                                "%s[[%s]]%s"
                                % (
                                    editList[i],
                                    diplList[i].replace("_", " "),
                                    separator,
                                )
                            )
                        else:
                            newLine.append("%s%s" % (editList[i], separator))
                        # input("%s :: %s" % (diplList[i], editList[i]))
                    # print(newLine)
                    newLine = "".join(newLine) + "[[in marg]]"

                    newText.append(newLine)

            # process folio information
            elif t.startswith("Folio"):
                # print("processing folio")
                # print(t)
                t = processFolio(t)
                newText.append(t)

            elif t.startswith("Page"):
                # print("processing page")
                # print(t)
                t = processPage(t)
                newText.append(t)

            # process
            elif t.startswith("#*#"):
                fnID = t[3:].split("::")[0].strip()
                fnBody = t[3:].split("::")[1].strip()
                footnotesData[fnID] = fnBody

            elif t.startswith("#+#"):
                fnID = t[3:].split("::")[0].strip()
                fnBody = t[3:].split("::")[1].strip()
                # footnotesData[fnID] = "<i>insert</i>: " + fnBody
                insertionsData[fnID] = fnBody
                editedText.replace(fnID, fnBody)

            elif t.startswith("#++#"):
                fnID = t[4:].split("::")[0].strip()
                fnBody = t[4:].split("::")[1].strip()
                # footnotesData[fnID] = "<i>insert</i>: " + fnBody
                marginalInsertionsData[fnID] = fnBody
                editedText.replace(fnID, fnBody)

            # catch errors
            else:
                pass
                print(t)
                print("Error in encoding...")

        editedText = " ".join(editedText.split())
        textFinal = "=====".join(newText)

        # process footnotes and comments
        footnotesFinal = []
        variants = []
        fnCounter = 0
        for k, v in footnotesData.items():
            fnCounter += 1
            # refMap = textFinal.count(k)
            refMap = len(re.findall(r"\b%s\b" % k, textFinal))
            # print(refMap)

            if refMap == 2:
                counterTemp = 0
                # print(k)
                lemma = (
                    re.sub(r"\b[A-Z]+[0-9]+\b", "", editedText.strip().split(k, 2)[1])
                    .strip()
                    .replace(".", "")
                    .replace(":", "")
                    .replace("،", "")
                    .replace("؟", "")
                )
                lemma = lemma
                # print(lemma)
                fnMrkr = "<span class='fnt'>" + intToRoman(fnCounter) + "</span>"
                fntMrkrCmt = (
                    "<span class='fntMrkrCmt'>" + intToRoman(fnCounter) + "</span>"
                )
                textFinal = re.sub(
                    r"\b%s\b(.*)\b%s\b" % (k, k),
                    r"%s\1%s" % ("", fntMrkrCmt),
                    textFinal,
                )

                # print("\b%s (.*) %s\b" % (k, k))
                brk = ". <br>" if not v.strip()[-1] == "." else " <br>"
                lemmaList = lemma.split(" ")
                if len(lemmaList) > 20:
                    shortLemma = (
                        " ".join(lemmaList[:5]) + " ... " + " ".join(lemmaList[-5:])
                    )
                    footNote = fnMrkr + " <span>" + shortLemma + "] </span>" + v + brk
                else:
                    footNote = fnMrkr + " <span>" + lemma + "] </span>" + v + brk
                footnotesFinal.append(footNote)
                # print(k)

            elif refMap == 1:
                counterTemp = 0
                # print(editedText.split(k)[0])
                lemma = (
                    (
                        re.sub(r"\b[A-Z]+[0-9]+\b", "", editedText.split(k)[0])
                        .strip()
                        .split()[-1]
                    )
                    .replace(".", "")
                    .replace(":", "")
                    .replace("،", "")
                    .replace("؟", "")
                )
                # print(lemma)
                fnMrkr = "<span class='fnt'>" + intToRoman(fnCounter) + "</span>"
                fntMrkrCmt = (
                    "<span class='fntMrkrCmt'>" + intToRoman(fnCounter) + "</span>"
                )
                textFinal = re.sub(r"\b%s\b" % (k), r"%s" % (fntMrkrCmt), textFinal)

                # footNote = m1 + " ... " + m2 + " : " + v + ".<br>"
                brk = ". <br>" if not v.strip()[-1] == "." else " <br>"
                footNote = fnMrkr + " <span>" + lemma + "] </span>" + v + brk
                footnotesFinal.append(footNote)
                # print(m1)

            else:
                # pass
                print(k, v)
                print("ERROR! ERROR! ERROR")

        # process insertions
        for k, v in insertionsData.items():
            r = v + f"[[omLEMMA {v}]]"
            # print(k, r)
            textFinal = textFinal.replace(k, r, 1)

        for k, v in marginalInsertionsData.items():
            r = v + f"[[mgLEMMA {v}]]"
            # print(k, r)
            textFinal = textFinal.replace(k, r, 1)

        # process variations
        # variants = []
        varCounter = 1
        # print(textFinal)
        # for i in re.finditer(r"\b([^\[^\b^\s]+\[\[[^\]]+\b\]\])", textFinal):
        for i in re.finditer(r"\b([^\s]+\[\[[^\]]+\]\])", textFinal):
            # print(i)
            matchV = i.group(1)
            replaceV = (
                matchV.split("[[")[0] + "<span class='fntMrkr'>%d</span>" % varCounter
            )
            variantFN = ""
            if "omLEMMA" in matchV[:-2].split("[[")[1]:
                # print(matchV[:-2].split("[[")[1].split("omLEMMA")[1].strip())
                variantFN = (
                    "<span class='fnt'>%d</span> " % varCounter
                    + matchV[:-2].split("[[")[1].split("omLEMMA")[1].strip()
                    + "<span class='om'>"
                    + "om"
                    + " [</span>."
                )
            elif "mgLEMMA" in matchV[:-2].split("[[")[1]:
                # print(matchV[:-2].split("[[")[1].split("omLEMMA")[1].strip())
                variantFN = (
                    "<span class='fnt'>%d</span> " % varCounter
                    + matchV[:-2].split("[[")[1].split("mgLEMMA")[1].strip()
                    + "<span class='om'>"
                    + "in marg"
                    + " [</span>."
                )
            elif matchV[:-2].split("[[")[1] == "in marg":
                variantFN = (
                    "<span class='fnt'>%d</span> " % varCounter
                    + matchV[:-2].split("[[")[0]
                    + "<span class='om'>"
                    + matchV[:-2].split("[[")[1]
                    + " [</span>."
                )
            else:
                variantFN = (
                    "<span class='fnt'>%d</span> " % varCounter
                    + matchV[:-2].split("[[")[0]
                    + "] "
                    + matchV[:-2].split("[[")[1]
                    + "."
                )
            variantFN = variantFN.replace("~~~", " <b><i>...</i></b>")
            textFinal = textFinal.replace(matchV, replaceV, 1)

            # print(variantFN)
            variants.append(variantFN)
            varCounter += 1

            # print()

        # print(textFinal)

        textFinal = textFinal.replace(
            " <span class='fntMrkrCmt'>", "<span class='fntMrkrCmt'>"
        )

        soup = BeautifulSoup(textFinal, "html.parser")
        for section in soup.find_all("span", {"class": "fntMrkr"}):
            nextNode = section
            while True:
                nextNode = nextNode.nextSibling
                try:
                    tag_name = nextNode.name
                except AttributeError:
                    tag_name = ""
                if tag_name == "span" and nextNode["class"][0] == "fntMrkrCmt":
                    nextNode.string = " ," + nextNode.string
                else:
                    break

        textFinal = str(soup)

        textFinal = textFinal.replace("=====", "\n")
        textFinal = "<p class='mainText'>\n\n%s\n\n</p>" % textFinal
        comments = (
            "<h3>Comments</h3>\n\n"
            + "<p class='comments'>\n\n%s\n\n</p>" % "\n".join(footnotesFinal)
        )
        variants = (
            "<h3>Variants</h3>\n\n"
            + "<p class='variants'>\n\n%s\n\n</p>" % "\n".join(variants)
        )
        metadata = (
            "<h3>Metadata</h3>\n\n" + "<p class='metadata'>\n\n%s\n\n</p>" % metadata
        )

        textFinal = textFinal + variants + comments + metadata

        # REMOVE SOME ELEMENTS
        textFinal = textFinal.replace("BR", "").replace("%", "").replace("[[]]", "")
        textFinal = textFinal.replace("INSERT_HERE", "<i>no data has been provided</i>")
        textFinal = re.sub("@[pt]\d+", "", textFinal)

        # print(textFinal)

        # INSERT IMAGES
        for k, v in imageDic.items():
            find = k.split(".")[0]
            repl = imageWrapper.replace("$HTMLPATH$", v["htmlPath"])
            # print(find, " >>>> ", repl)
            # input()
            # textFinal = textFinal.replace(find, repl)
            textFinal = re.sub(r"\b%s\b" % find, repl, textFinal)

        with open(sourceFolder + "template_index.html", "r", encoding="utf8") as f1:
            template = f1.read()

        template = template.replace("@MAINCONTENT@", textFinal)

        with open(
            pathToFile.replace(".mARkdownMSS", ".html"), "w", encoding="utf8"
        ) as f9:
            f9.write(template)


##########################################################################
# RUNNING ################################################################
##########################################################################

files = []
for f in sorted(os.listdir(sourceFolder)):
    if f == "":
        break
    else:
        if (
            not f.startswith(".")
            and f.endswith(".mARkdownMSS")
            # and "1280CumarIbnSayyid.Risala1819.YaleJWJ185xD1-ara1" in f
        ):
            print("## ", f)
            converter(sourceFolder + f)

##########################################################################
# REFERENCES #############################################################
##########################################################################
# http://jsfiddle.net/4hzenxkh/1/ - CSS example of image popup (no JS)
##########################################################################
