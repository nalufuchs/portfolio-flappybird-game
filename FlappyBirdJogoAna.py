import pygame
import os
import random


TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'bg.png')))
IMAGENS_PASSARO =[
pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'bird1.png'))),
pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'bird2.png'))),
pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'bird3.png')))
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


class Passaro:
    IMGS = IMAGENS_PASSARO
    #animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5 #parametro pra verificar de 5 em 5 frames a animação

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0  #variável do pulo, o deslocamento/decaimento do pássaro
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]


    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0  #o pássaro, ao pular, ele zera o deslocamento
        self.altura = self.y

    def mover(self):
        #Calcular o deslocamento
        self.tempo +=1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        #Restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
            #facilitar a jogabilidade para subir mais rápido

        self.y += deslocamento

        #Angulo do pássaro para a animação de cair
        if deslocamento < 0 or self.y < (self.altura + 50):
        #Ao pular, o deslocamento será negativo, então o ângulo vai ser para cima
        #O self.y serve para que, enquanto a altura dele ainda estiver antes da altura que ele estava, ele permanecer apontado para cima
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
                #Se o pássaro tá pulando, a rotação para cima dele é a máxima
        else:
            #Ele vai cair o ângulo, mas tem que limitar pro pássaro não dar uma pirueta
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO


    def desenhar(self, tela): #Funcao para desenhar o pássaro no inicio
        #Definir qual imagem do pássaro vai usar
        #A cada contagem de imagem (tempo de animação) ele baterá asa
        self.contagem_imagem +=1

        if self.contagem_imagem < self.TEMPO_ANIMACAO: #ASA PRA CIMA
            self.imagem = self.IMGS[0]
        #Se a contagem for menor que o tempo de animação, troca de imagem
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2: #Asa pro meio
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3: #Asa pra baixo
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4: #asa pro meio
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 +1: #asa pro meio
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0  #Reseta a contagem pra ele subir de novo a asa


        #Se o pássaro tiver caindo, não precisa bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]  #se tá caindo, a asa tá pra baixo
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2



        #desenhar imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo) #imagem e qtos graus
        centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=centro_imagem)

        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)
        #Verificação dos pixeis da imagem e não do retangulo total


class Cano:
    DISTANCIA = 200 #Distancia fixa entre o cano superior e inferior
    VELOCIDADE = 5

    def __init__(self, x):
        #Apenas posicao X pq ele vai estar fixo na tela, a altura é aleatória
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False  #Se o pássaro passou o cano
        self.definir_altura() #funcao init roda automatico, já chamando a funcao definir altura pra definir as alturas do cano

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        #altura entre 50 e 450 para criar um intervalo dos 800 pixeis e evitar que saia um cano muito alto e outro muito longe
        self.pos_topo = self.altura - self.CANO_TOPO.get_height() #negativo pq o Y é neg e MENOS a altura do cano
        self.pos_base = self.altura + self.DISTANCIA

    #Definir a velocidade do cano, porque ele não acelera nem nada, ele é constante
    def mover(self):
        self.x -= self.VELOCIDADE   #Como o eixo x cresce para direita, e vc quer q ele vá pra esquesquerda, vc tem que REDUZIR o valor de x

    def desenhar(self, tela): #Desenhar o cano, ele n precisa fazer nada pq já foi feito o inverso lá no inicio, é só "blitar" ele
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo)) #O comando pede o que quero desenhar, o eixo x e Y (tupla)
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))    #Porém como o cano no eixo Y varia sua ALTURA, o Y = posicao_topo ou posicao_base

    def colidir(self, passaro):
        #Verificar se a máscara criada do pássaro, máscara do cano de cima e de baixo e ver se tá condizente
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        #Verificar se há colisão com a distancia do pássaro pro cano do topo e da base (mask)
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y)) #EIXO X e EIXO Y = diferença do cano pro passaro no eixo X e Y
        #Deve ser arredondado porque o nr do passaro, por culpa da formula, é mt quebrado
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        #Método de verificação da colisão
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)  #Serão true ou false
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)  #Se existir colisao

        #Método retorna colisão sim ou não, true ou false
        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 5 #Velocidade constante, = a do cano
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO
    #Para evitar que a primeira imagem do chao suma e fique vazio, deve ser adicionado uma nova imagem (chao2) para ser sempre criada após pro chao nao ficar vazio

    def __init__(self, y): #Precisa só do Y pq a funcao init vai determinar o X do chao1 pra adicionar o chao2 no final
        self.y = y
        self.x1 = 0 #X do chao1, 0 pq ele começa zerado
        '''self.x2 = self.x1 + self.LARGURA'''  #X do chao2 = largura do chao1 + onde o chao1 começou
                    #o self.x1 é = a 0, então pode ser removido
        self.x2 = self.LARGURA
        #ao iniciar o jogo, já vão estar uma do lado da outra. Agora, verifica-se uma função para mover


    def mover(self):  #Negativo pq o chão vai pra trás no X, já que x cresce pra direita
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            #Ou seja, se ele está menor que zero que é o eixo X incial, ele saiu da tela
            self.x1 = self.x2 + self.LARGURA #quando ele sair do eixo 0, ele vai ser igualado à largura (vai pro final)
            #Exatamente igual lá no início com x2, porém com x1
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA


    def desenhar(self, tela):
        #Como nao tem q rotacionar nem nada, só copiar o tela.blit do cano
        tela.blit(self.IMAGEM, (self.x1, self.y))  # O comando pede o que quero desenhar, o eixo x e Y (tupla)
        tela.blit(self.IMAGEM, (self.x2, self.y)) #O eixo Y é fixo



#Agora função para desenhar o jogo.

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0)) #imagem que quer desenhar e eixos X e Y, que no caso 0 e 0 pq quero q comece
    for passaro in passaros:  #Caso exista mais de um pássaro
        passaro.desenhar(tela) #funcao para desenhar feita já

    for cano in canos: #Existe mais de uma dupla de canos na tela ao mesmo tempo
        cano.desenhar(tela)

    #Criar o texto na tela, usar a função render
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))  #Onde o texto fica, eixo X é o texto + espacinho pro fim da tela e Y é fixo
    chao.desenhar(tela)
    pygame.display.update()



def main():
    #Passaros é uma instância da classe de pássaros criada
    passaros = [Passaro(230, 350)] #A funcao exige onde o pássaro vai aparecer na tela, entao os valores foram escolhidos por teste
    chao = Chao(730)  #Apenas o eixo Y que aparece, e essa é fixa
    canos = [Cano(700)] #Lista de canos, e passa apenas a posição X já que a Y é definida aleatoriamente (começa no final da tela)
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA)) #criacao da tela, tamanho da largura e altura
    pontos = 0   #O texto é escrito no desenhar tela, mas o parâmetro deve ser na main
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:  #Jogo é um loop infinito, até o usuário fechar
        relogio.tick(30)  #Qtos frames por segundo ele irá atualizar, 30 é ok

        #Como interagir com o jogador, o pygame detecta eventos (clicar, espaço, etc)
        #Porém tudo pode ser um evento, clicar, espaço, etc. Então deve detectar o que quer:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: #se o evento for clicar no X de fechar
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN: #Keydown é apertar alguma tecla, então detectar se é o espaço
                if evento.key == pygame.K_SPACE:  #Apertar o espaço
                    #O pássaro é uma lista de pássaros, então:
                    for passaro in passaros:
                        passaro.pular()

        #Mover as coisas
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        #Ao mover o cano, deve tomar cuidado para criar um novo caso o pássaro já tenha passado dele
        #Ou se ele bateu com o cano, encerrar a fase
        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            #Para cada cano, verificar se bateu num pássaro:
            for i, passaro in enumerate(passaros): #Percorrer a lista de pássaros
                #Para eliminar o pássaro, deve saber a posição dele na lista (i)
                if cano.colidir(passaro):
                    passaros.pop(i) #Se ele não passou do cano
                if not cano.passou and passaro.x > cano.x:
                #Se a variável cano.passou é falsa + o X do pássaro é MAIOR que o X do cano (ou seja, ele tem um X positivo, passou do cano)
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()  #O cano deve mover-se
            #Deve verificar se ele já passou da tela (não ta mais visível)
            #Ou seja, que nem no chão: se a posição dele (x) + a largura < 0
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                #Ao invés de excluir direto, vamos adicionar a uma lista pra excluir
                remover_canos.append(cano)
                #pq nao exclui direto? pq como tá no for, ele tá num loop, pode ocorrer de deixar de excluir algum pq qdo o loop passou ele n tava no parametro

        #Depois de percorrer TODA a lista de canos, adiciona e exclui quem precisa:
        if adicionar_cano:
            pontos +=1
            canos.append(Cano(600)) #O cano vai começar a vir um pouco próximo da tela (que é 500)

        #Remover o cano
        for cano in remover_canos:
            canos.remove(cano)

        #Definir as colisões com céu e chão: se a altura dele for maior que teto ou menor que chão
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
            # Posicao do chao ou a altura dele (y é o top maior de altura) for menor que 0 (maximo Y):
        desenhar_tela(tela, passaros, canos, chao, pontos)



#Executar a função, ele vai rodar
#main()

#Mas usualmente se faz assim:
if __name__ == '__main__':
    main()
#Serve pra questão de segurança para caso importe algum arquivo ele não rode sem um clique proposital
#Ao executar o script, coloca-se  ele dentro de uma função name main





