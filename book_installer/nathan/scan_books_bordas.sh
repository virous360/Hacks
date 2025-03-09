#!/bin/bash

SCRIPTFULLNAME=$(realpath "$0")
SCRIPTPATH=$(dirname "${SCRIPTFULLNAME}")
SCRIPTNAME=$(basename "${SCRIPTFULLNAME}")

function usage
{
	echo "Usage:"
	echo "${0} [-cat <cat-id>] [-book <book-id>] [-book-timer <wait timer beetween books>] [-force]"
	exit ${1}
}

BOOKCAT=$(seq 1 9)
BOOKID=$(seq 1000 4000)
BORDAS_FILLING="2edc59852fc64cc6b917bba10061dde7bc3ed8af4f5a69eb6ef848a6800e6bab81c95f9a6bfbeb86"
FORCE_DOWNLOAD=false
BOOK_TIMER=5

# https://biblio.editions-bordas.fr/epubs/web/1e9ca049e22eec903fd69d44827b99fd4b02031c172447d04b15b5c5b8bd5b50ebe82fb331b24d5f/BORDAS/bibliomanuels/distrib_gp/1/4/3013/online/OEBPS/chapter_1/
# bookcat = 4
# bookid = 3013
# https://biblio.editions-bordas.fr/epubs/web/2edc59852fc64cc6b917bba10061dde7bc3ed8af4f5a69eb6ef848a6800e6bab81c95f9a6bfbeb86/BORDAS/bibliomanuels/distrib_gp/1/9/8655/online/OEBPS/Chapter_001/

while [ $# -gt 0 ]
do
	case "$1" in
		-c | --c | -cat | --cat )
			shift
			BOOKCAT="${1}"
			;;
		-b | --b | -book | --book )
			shift
			BOOKID="${1}"
			;;
		-book-timer | --book-timer )
			shift
			BOOK_TIMER="${1}"
			;;
		-force | --force )
			FORCE_DOWNLOAD=true
			;;
		-? | --? | -h | --h | -help | --help )
			usage "0"
			;;
		*)
			echo "ERROR: Unknown argument '$1'!"
			usage "1"
			;;
	esac
	shift
done

function processBook
{
	echo "	-> Found book #${3} (${1}/${2})"
	BOOK_TAR="${SCRIPTPATH}/${1}_${2}_${3}.tar.gz"
	BOOK_DIR="${SCRIPTPATH}/${1}/${2}/${3}"
	if [ ${FORCE_DOWNLOAD} == true ] && [ -f "${BOOK_TAR}" ]
	then
		rm -rf ${BOOK_TAR}
	fi
	if [ ! -f "${BOOK_TAR}" ];
	then
		echo "		-> Storage folder: ${BOOK_DIR}"
		mkdir -p ${BOOK_DIR}

		# curl -sS -q -o ${BOOK_DIR}/content.txt https://biblio.editions-bordas.fr/epubs/web/${BORDAS_FILLING}/BORDAS/bibliomanuels/distrib_gp/${1}/${2}/${3}/online/OEBPS/content.opf 
		# echo https://biblio.editions-bordas.fr/epubs/web/${BORDAS_FILLING}/BORDAS/bibliomanuels/distrib_gp/${1}/${2}/${3}/online/OEBPS/content.opf 

		BOOK_TITLE=`cat ${BOOK_DIR}/content.txt | grep "<dc:title id=\"title1\">" | awk -F'>' '{ print $2 }' | awk -F'<' '{ print $1 }'`
		BOOK_IDENTIFIER=`cat ${BOOK_DIR}/content.txt | grep "<dc:identifier " | awk -F'>' '{ print $2 }' | awk -F'<' '{ print $1 }'`
		# BOOK_PAGELIST=`cat ${BOOK_DIR}/content.txt | grep "\.xhtml" | grep "Page" | awk -F'href="' '{ print $2 }' | awk -F'"' '{ print $1 }' | tr '\n' ',' | sed 's#,#","#g'`
		BOOK_PAGELIST=`cat ${BOOK_DIR}/content.txt | grep "\.jpg" | grep "Page" | awk -F'href="' '{ print $2 }' | awk -F'"' '{ print $1 }' | tr '\n' ',' | sed 's#,#","#g'`
		
		if [ "x${BOOK_PAGELIST}" != "x" ]
		then
			BOOK_PAGELIST="\"${BOOK_PAGELIST:0:-2}"
			for file in `cat ${BOOK_DIR}/content.txt | grep "<item " | awk -F'href=' '{ print $2 }' | awk -F'"' '{ print $2 }'`
			do
				RESSOURCE_FOLDER=`dirname $file`
				RESSOURCE_NAME=`basename $file`
				mkdir -p ${BOOK_DIR}/${RESSOURCE_FOLDER}
				echo "		# Processing file: ${RESSOURCE_NAME} (target: /${RESSOURCE_FOLDER})"
				curl -sS -q -o ${BOOK_DIR}/${RESSOURCE_FOLDER}/${RESSOURCE_NAME} https://biblio.editions-bordas.fr/epubs/web/${BORDAS_FILLING}/BORDAS/bibliomanuels/distrib_gp/${1}/${2}/${3}/online/OEBPS/${file} || echo "			! ERROR"
			done

			echo "		-> Downloading epub"
			curl -sS -q -o ${BOOK_DIR}/book.epub http://dl.editions-bordas.fr//BORDAS/bibliomanuels/distrib_gp/${1}/${2}/${3}/${3}-1_2-${BOOK_IDENTIFIER}.epub

			echo "		-> Building archive"
			cp ${SCRIPTPATH}/index.html ${BOOK_DIR}
			cat ${BOOK_DIR}/index.html | sed "s#{{ title }}#${BOOK_TITLE}#g" > ${BOOK_DIR}/index.html.tmp && mv ${BOOK_DIR}/index.html.tmp ${BOOK_DIR}/index.html
			cat ${BOOK_DIR}/index.html | sed "s#{{ pagelist }}#${BOOK_PAGELIST}#g" > ${BOOK_DIR}/index.html.tmp && mv ${BOOK_DIR}/index.html.tmp ${BOOK_DIR}/index.html
			cd ${BOOK_DIR}
			tar czvf ${BOOK_TAR} *
			cd -
			echo "		-> Generated archive: ${BOOK_TAR}"
			rm -rf ${BOOK_DIR}
		else
			echo "Failed! Book seems to have gotten away..."
		fi

		echo "		-> Breezing"
		sleep ${BOOK_TIMER}
	else
		echo "		[SKIPPED]"
	fi
}

for bookcat in ${BOOKCAT}
do
	for book in ${BOOKID}
	do
		echo "Scanning ${book}"
		curl -sS -q -o /dev/null https://biblio.editions-bordas.fr/epubs/web/${BORDAS_FILLING}/BORDAS/bibliomanuels/distrib_gp/1/${bookcat}/${book}/online/OEBPS/content.opf  && processBook 1 ${bookcat} ${book}
	done
done

echo "eop."