import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

/** Benchmark do KMP em Java usando System.nanoTime(). */
public class BenchmarkKMP {
    private static final String[] TAMANHOS_NOME = {"pequena", "media", "grande"};
    private static final int[] TAMANHOS_N = {1_000, 10_000, 100_000};
    private static final String[] CENARIOS = {"melhor", "medio", "pior"};
    private static final String ALFABETO_VARIADO = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    private static final String PADRAO_MELHOR = "KMPBUSCAEFICIENTE";
    private static final String PADRAO_PIOR = "aaaaab";
    private static final int TAMANHO_PADRAO_MEDIO = 32;

    private record Entrada(String tamanhoNome, int n, String cenario, String texto, String padrao) {}

    private static String lcgCaracteres(int tamanho, int seed, String alfabeto) {
        long estado = seed & 0x7FFFFFFFL;
        StringBuilder sb = new StringBuilder(tamanho);

        for (int i = 0; i < tamanho; i++) {
            estado = (1103515245L * estado + 12345L) & 0x7FFFFFFFL;
            sb.append(alfabeto.charAt((int) (estado % alfabeto.length())));
        }

        return sb.toString();
    }

    private static Entrada gerarEntrada(String tamanhoNome, int n, String cenario) {
        String texto;
        String padrao;

        if (cenario.equals("melhor")) {
            padrao = PADRAO_MELHOR;
            int restante = Math.max(0, n - padrao.length());
            texto = padrao + lcgCaracteres(restante, n + 101, "bcdefghijklmnopqrstuvwxyz");
        } else if (cenario.equals("medio")) {
            padrao = lcgCaracteres(TAMANHO_PADRAO_MEDIO, n * 17 + 13, ALFABETO_VARIADO);
            texto = lcgCaracteres(n, n * 31 + 7, ALFABETO_VARIADO);
        } else {
            padrao = PADRAO_PIOR;
            texto = "a".repeat(n);
        }

        return new Entrada(tamanhoNome, n, cenario, texto, padrao);
    }

    public static void main(String[] args) throws IOException {
        Locale.setDefault(Locale.US);
        int runs = args.length > 0 ? Integer.parseInt(args[0]) : 30;
        if (runs <= 0) {
            throw new IllegalArgumentException("runs deve ser maior que zero");
        }

        Path resultados = Path.of("resultados");
        Files.createDirectories(resultados);
        Path saida = resultados.resolve("resultados_java.csv");

        try (BufferedWriter writer = Files.newBufferedWriter(saida, StandardCharsets.UTF_8)) {
            writer.write("linguagem,tamanho_nome,tamanho_n,cenario,repeticao,padrao_m,ocorrencias,tempo_segundos,tempo_ns");
            writer.newLine();

            for (int t = 0; t < TAMANHOS_N.length; t++) {
                for (String cenario : CENARIOS) {
                    Entrada entrada = gerarEntrada(TAMANHOS_NOME[t], TAMANHOS_N[t], cenario);

                    // Aquecimento simples fora das medicoes registradas.
                    KMP.contarOcorrencias(entrada.texto(), entrada.padrao());

                    for (int repeticao = 1; repeticao <= runs; repeticao++) {
                        long inicio = System.nanoTime();
                        int ocorrencias = KMP.contarOcorrencias(entrada.texto(), entrada.padrao());
                        long fim = System.nanoTime();

                        long tempoNs = fim - inicio;
                        double tempoSegundos = tempoNs / 1_000_000_000.0;

                        writer.write(String.format(
                            Locale.US,
                            "Java,%s,%d,%s,%d,%d,%d,%.12f,%d",
                            entrada.tamanhoNome(),
                            entrada.n(),
                            entrada.cenario(),
                            repeticao,
                            entrada.padrao().length(),
                            ocorrencias,
                            tempoSegundos,
                            tempoNs
                        ));
                        writer.newLine();
                    }
                }
            }
        }

        System.out.println("Benchmark Java salvo em: " + saida.toAbsolutePath());
    }
}
