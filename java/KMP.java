import java.util.ArrayList;
import java.util.List;

/** Implementacao didatica do algoritmo Knuth-Morris-Pratt (KMP). */
public class KMP {
    public static int[] construirLps(String padrao) {
        int[] lps = new int[padrao.length()];
        int tamanhoPrefixo = 0;
        int i = 1;

        while (i < padrao.length()) {
            if (padrao.charAt(i) == padrao.charAt(tamanhoPrefixo)) {
                tamanhoPrefixo++;
                lps[i] = tamanhoPrefixo;
                i++;
            } else if (tamanhoPrefixo != 0) {
                tamanhoPrefixo = lps[tamanhoPrefixo - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }

        return lps;
    }

    public static List<Integer> buscar(String texto, String padrao) {
        List<Integer> ocorrencias = new ArrayList<>();
        if (padrao.isEmpty()) {
            for (int i = 0; i <= texto.length(); i++) {
                ocorrencias.add(i);
            }
            return ocorrencias;
        }

        int[] lps = construirLps(padrao);
        int i = 0;
        int j = 0;

        while (i < texto.length()) {
            if (texto.charAt(i) == padrao.charAt(j)) {
                i++;
                j++;

                if (j == padrao.length()) {
                    ocorrencias.add(i - j);
                    j = lps[j - 1];
                }
            } else if (j != 0) {
                j = lps[j - 1];
            } else {
                i++;
            }
        }

        return ocorrencias;
    }

    public static int contarOcorrencias(String texto, String padrao) {
        return buscar(texto, padrao).size();
    }

    public static void main(String[] args) {
        String texto = "ababcabcabababd";
        String padrao = "ababd";
        System.out.println("Ocorrencias: " + buscar(texto, padrao));
    }
}
