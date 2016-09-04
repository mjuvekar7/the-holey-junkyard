/* Generated By:JJTree: Do not edit this line. ASTroot.java Version 6.1 */
/* JavaCCOptions:MULTI=true,NODE_USES_PARSER=false,VISITOR=false,TRACK_TOKENS=false,NODE_PREFIX=AST,NODE_EXTENDS=,NODE_FACTORY=,SUPPORT_CLASS_VISIBILITY_PUBLIC=true */
public class ASTroot extends SimpleNode {
    public ASTroot(int id) {
        super(id);
    }

    public ASTroot(GoDlangParser p, int id) {
        super(p, id);
    }
  
    public void translate(int indent) throws UnsupportedOperationException {
        output(indent, "import java.util.ArrayList;\n");
        output(indent, "public class " + name + " {\n");
        indent++;
        for (int i = 0; i < jjtGetNumChildren(); i++) {
            ((SimpleNode) jjtGetChild(i)).translate(indent);
        }
        indent--;
        output(indent, "}\n");
    }
  
    public void semanticCheck() throws ParseException, UnsupportedOperationException {
        // nothing special for root
        for (int i = 0; i < jjtGetNumChildren(); i++) {
            ((SimpleNode) jjtGetChild(i)).semanticCheck();
        }
    }
}
/* JavaCC - OriginalChecksum=0f6d9ba41b9d5fc39c69f39fc575081b (do not edit this line) */
