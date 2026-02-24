import java.util.Scanner;

public class ChatBot {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Chatbot Simulado (Java) - digite 'sair' para encerrar.");
        while (true) {
            System.out.print("Você: ");
            String line = sc.nextLine();
            if (line == null) break;
            line = line.trim();
            if (line.equalsIgnoreCase("sair")) break;
            String low = line.toLowerCase();
            String reply;
            if (low.isEmpty()) reply = "Diga algo sobre seu pedido ou produto.";
            else if (low.contains("frete") || low.contains("entrega") || low.contains("cep")) reply = "Posso ajudar com frete. Qual é seu CEP?";
            else if (low.contains("troca") || low.contains("devol")) reply = "Trocas até 30 dias. Deseja iniciar?";
            else if (low.contains("pag") || low.contains("cartão") || low.contains("boleto")) reply = "Aceitamos cartão e boleto. Precisa de ajuda no pagamento?";
            else reply = "Simulação IA: você disse '" + line + "'. Como posso ajudar mais?";
            System.out.println("Bot: " + reply);
        }
        sc.close();
        System.out.println("Encerrando chatbot Java.");
    }
}
