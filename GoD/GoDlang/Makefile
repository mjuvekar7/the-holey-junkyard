customs = GoDlang.jjt AST*.java SimpleNode.java
.PHONY = parser clean

parser: $(customs)
	mkdir -p aux
	cp $(customs) aux/
	cd aux/ && \
	jjtree GoDlang.jjt && \
	javacc GoDlang.jj && \
	javac GoDlangParser.java && \
	cp GoDlangParser.class ../

clean:
	rm -r aux/
