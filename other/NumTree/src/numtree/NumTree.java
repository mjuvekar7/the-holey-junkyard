package numtree;

import java.math.BigInteger;
import java.util.*;

public class NumTree {

    private static HashMap<Threeple, Node> existing = new HashMap<>(100);
    private static final int RUNS = 50;
    private static final int IGNORES = 10;

    public static void main(String[] args) {
        Random r = new Random();
        int rand;
        long total = 0, max = 0, start, end, diff;
        for (int i = 0; i < RUNS; i++) {
            rand = r.nextInt(12500) + 1;
//            System.out.print(rand + ": ");

            start = System.nanoTime();
            Node n = getKth(rand);
            end = System.nanoTime();
            diff = end - start;

//            System.out.println(n);
            if (i > IGNORES) {
                if (diff > max) {
                    max = diff;
                }
                total += diff;
            }
        }
        System.out.println(Double.toString((double) total / ((RUNS - IGNORES) * 1_000_000_000L)));
        System.out.println(Double.toString((double) max / 1_000_000_000L));
    }

    private static Node getKth(int k) {
        existing.forEach((Threeple t, Node n) -> {
            n.two = false;
            n.three = false;
        });
        ArrayList<Node> opens = new ArrayList<>();
        Node root = Node.getNode(0, 0, 0);
        opens.add(root);
        Node curmin = null;

        ArrayList<Node> tries = new ArrayList<>();
        for (int i = 0; i < k; i++) {
            tries.clear();
            opens.stream().forEach((Node n) -> {
                int a = n.t.getA();
                int b = n.t.getB();
                int c = n.t.getC();
                if (!n.two) {
                    tries.add(Node.getNode(a + 1, b, c));
                }
                if (!n.three) {
                    tries.add(Node.getNode(a, b + 1, c));
                }
                tries.add(Node.getNode(a, b, c + 1));
            });

            Optional<Node> min = tries.stream().min((Node m, Node n) -> {
                return m.t.getValue().compareTo(n.t.getValue());
            });
            curmin = min.get();
            opens.add(curmin);

            int a = curmin.t.getA();
            int b = curmin.t.getB();
            int c = curmin.t.getC();
            if (a - 1 >= 0) {
                Node.getNode(a - 1, b, c).two = true;
            }
            if (b - 1 >= 0) {
                Node.getNode(a, b - 1, c).three = true;
            }
            if (c - 1 >= 0) {
                opens.remove(Node.getNode(a, b, c - 1));
            }
        }
        return curmin;
    }

    static class Threeple {

        private BigInteger value;
        private final int hash;
        private final int a;
        private final int b;
        private final int c;
        private static final BigInteger TWO = new BigInteger("2");
        private static final BigInteger THREE = new BigInteger("3");
        private static final BigInteger FIVE = new BigInteger("5");

        Threeple(int x, int y, int z, boolean calc) {
            a = x;
            b = y;
            c = z;
            hash = hashThis();
            if (calc) {
                calcValue();
            }
        }

        public void calcValue() {
            value = TWO.pow(a).multiply(THREE.pow(b)).multiply(FIVE.pow(c));
        }

        public int getA() {
            return a;
        }

        public int getB() {
            return b;
        }

        public int getC() {
            return c;
        }

        public BigInteger getValue() {
            return value;
        }

        @Override
        public int hashCode() {
            return hash;
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) {
                return true;
            }
            if (obj == null) {
                return false;
            }
            if (getClass() != obj.getClass()) {
                return false;
            }
            final Threeple other = (Threeple) obj;
            if (this.a != other.getA()) {
                return false;
            }
            if (this.b != other.getB()) {
                return false;
            }
            if (this.c != other.getC()) {
                return false;
            }
            return true;
        }

        private int hashThis() {
            int hashVal = 7;
            hashVal = 37 * hashVal + c;
            hashVal = 37 * hashVal + b;
            hashVal = 37 * hashVal + a;
            return hashVal;
        }
    }

    static class Node {

        public Threeple t;
        public boolean two, three;

        private Node(int a, int b, int c) {
            t = new Threeple(a, b, c, true);
        }

        private Node(Threeple s) {
            t = s;
        }

        @Override
        public String toString() {
            return "(" + t.getA() + ", " + t.getB() + ", " + t.getC() + ")";
        }

        public static Node getNode(int a, int b, int c) {
            Threeple s = new Threeple(a, b, c, false);
            Node ret = existing.get(s);
            if (ret == null) {
                s.calcValue();
                Node act = new Node(s);
                existing.put(s, act);
                return act;
            }
            return ret;
        }
    }
}
