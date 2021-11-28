import pygame, sys, random

from pygame import transform
from pygame.display import flip

#hàm tạo mới floor và đẩy lên form
def newFloor():
    form.blit(floor, (floorMove, 520))
    form.blit(floor, (floorMove+400, 520))

#hàm kiểm tra va chạm:
def collisionHanding(obstaclces):
    for obstacle in obstaclces:
        if  birdRectangle.colliderect(obstacle):
            collisionSound.play()
            return False
    if birdRectangle.bottom >= 520:
        collisionSound.play()
        return False
    return True

# hàm tạo chuyển động lên xuống cho chim
def rotateBird(bird1):
    newBird = pygame.transform.rotozoom(bird1, - birdMovement*3, 1)
    return newBird

#hàm tạo hiệu ứng đập cánh
def birdAnimation():
    new_bird = bird_list[birdIndex] 
    new_birdRectangle = new_bird.get_rect(center = (100, birdRectangle.centery))
    return new_bird, new_birdRectangle

#hàm tính & hiển thị điểm
def show_score(gameStatus):
    if  gameStatus == 'running':
        scoreFormat = font_score.render(f'{int(score)}', True, (255,255,255))
        scoreRectangle = scoreFormat.get_rect(center = (200,100))
        form.blit(scoreFormat, scoreRectangle)
    if gameStatus == 'game over':
        #hiển thị điểm
        scoreFormat = font_score.render(f'Score: {int(score)}', True, (255,255,255))
        scoreRectangle = scoreFormat.get_rect(center = (200,150))
        form.blit(scoreFormat, scoreRectangle)
        
        #hiển thị điểm cao nhất
        highScoreFormat = font_score.render(f'Highest Score: {int(highest_score)}', True, (255,255,255))
        highScoreRectangle = highScoreFormat.get_rect(center = (200,450))
        form.blit(highScoreFormat, highScoreRectangle)

#hàm cập nhật điểm cao:
def updateScore(score, highScore):
    if score > highScore:
        highScore = score
    return highScore

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
#khởi tạo
pygame.init()

#Các biến dùng trong trò chơi:
floorMove = 0   #tọa độ x của 'floor'
g = 0.3     #biến trọng lực (gravity) để tạo chuyển động lên xuống cho chim
birdMovement = 0    #biến mô tả sự di chuyển của chim
check = True    #biến dừng trò chơi khi xảy ra va chạm
score = 0       #biến tính điểm
highest_score = 0   #điểm cao nhất
obsForm1_locate_x = 401     #tọa độ x của cột 1
obsForm2_locate_x = 601     #tọa độ x của cột 2
obsForm3_locate_x = 801     #tọa độ x của cột 3
obsForm_move = 3    #biến mô tả sự di chuyển của chướng ngại vật

obsForm1_locate_y = random.randint(250, 450)     #chiều cao random của cột 1
obsForm2_locate_y = random.randint(250, 450)    #chiều cao random của cột 2
obsForm3_locate_y = random.randint(250, 450)    #chiều cao random của cột 3

obsForm1_pass = False       #các biến kiểm tra tính điểm
obsForm2_pass = False       
obsForm3_pass = False
listOfObs = []


#khởi tạo 1 cửa sổ game với kích thước 250x400
form = pygame.display.set_mode((400, 600))  
#tên của form game
pygame.display.set_caption("FLAPPY BIRD")
#thiết lập fps 
fps = pygame.time.Clock()
#chọn ảnh làm background của game
background = pygame.image.load("Images/background-night.png")
#chỉnh kích cỡ ảnh phù hợp với form game
background = pygame.transform.smoothscale(background, (400,600))
#chọn ảnh làm nền phía dưới của game
floor = pygame.image.load("Images/newFloor.png")
#Chỉnh lại kích cỡ ảnh nền dưới(tăng kích thước lên 2 lần)
floor = pygame.transform.scale2x(floor)
#Thiết lập font chữ
font_score = pygame.font.Font('04B_19.TTF', 40)

#tạo chim
birdUp = pygame.image.load("Images/yellowbird-upflap.png")  #chọn ảnh con chim có cánh ở trên
birdMid = pygame.image.load("Images/yellowbird-midflap.png")  #chọn ảnh con chim có cánh ở giữa
birdDown = pygame.image.load("Images/yellowbird-downflap.png")  #chọn ảnh con chim có cánh ở dưới
bird_list = [birdUp, birdMid, birdDown]
birdIndex = 1
bird = bird_list[birdIndex]
#bird = pygame.image.load("Images/yellowbird-midflap.png")   #chọn ảnh con chim có cánh ở giữa
birdRectangle = bird.get_rect(center = (100,300))   #tạo khung HCN bên ngoài con chim

#tạo timer đập cánh cho chim
birdFlap = pygame.USEREVENT + 1
pygame.time.set_timer(birdFlap, 100)

#danh sách chiều cao ngẫu nhiên cho các chướng ngại vật
obsLength = [250,275,300,325,350,375,400,425,450]

#tạo các chướng ngại vật (obstacle)
obsForm = pygame.image.load("Images/obstacle.png")      #chọn ảnh chướng ngại vật
obsForm = pygame.transform.scale(obsForm, (41,350))     #quy định kích thước của chướng ngại vật
obsForm_flip = pygame.image.load("Images/obstacle_flip.png")    #chọn ảnh lật ngược chướng ngại vật

#tạo màn hình kết thúc
gameOver = pygame.image.load("Images/message.png")
gameOverRectangle = gameOver.get_rect(center = (200,300))

#chèn âm thanh
flapSound = pygame.mixer.Sound('sound/sfx_wing.wav')    #tiếng đập cánh
collisionSound = pygame.mixer.Sound('sound/sfx_hit.wav')    #tiếng va chạm với cột
scoreSound = pygame.mixer.Sound('sound/sfx_point.wav')      #tiếng ghi điểm

while True: #vòng lặp game
    for event in pygame.event.get(): #bắt tất cả các sự kiện diễn ra trong game(như bấm nút, va phải cột....)
        #tạo phím để thoát khỏi cửa sổ game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #tạo event bấm phím. Mỗi khi event được gọi, chim sẽ được bay lên
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and check:
                birdMovement = 0
                birdMovement = -5
                flapSound.play()
            if event.key == pygame.K_SPACE and check == False:
                check = True
                listOfObs.clear()
                birdRectangle.center = (100,350)
                birdMovement = 0
                score = 0
                obsForm1_locate_x = 401     #đặt lại tọa độ x của cột 1
                obsForm2_locate_x = 601     #đặt lại tọa độ x của cột 2
                obsForm3_locate_x = 801     #đặt lại tọa độ x của cột 3
                obsForm_move = 3
        
        #hiệu ứng đập cánh
        if event.type == birdFlap:
            if  birdIndex < 2:
                birdIndex+=1
            else:
                birdIndex = 0
            bird, birdRectangle = birdAnimation()
    form.blit(background, (0,0))   #tải background lên cửa sổ game tại tọa độ (0,0)

    #chướng ngại vật 1  
    obsForm1 = pygame.transform.scale(obsForm, (41,obsForm1_locate_y)) #cột dưới
    obsForm1 = form.blit(obsForm1, (obsForm1_locate_x, obsForm1_locate_y))

    obsForm1_flip_img = pygame.transform.scale(obsForm_flip, (41, obsForm1_locate_y-100)) #cột trên
    obsForm1_flip = form.blit(obsForm1_flip_img, (obsForm1_locate_x, 0))
    obsForm1_locate_x -= obsForm_move  #di chuyển obs1 sang trái

    #chướng ngại vật 2
    obsForm2 = pygame.transform.scale(obsForm, (41,obsForm2_locate_y))      #cột dưới
    obsForm2 = form.blit(obsForm2, (obsForm2_locate_x, obsForm2_locate_y))

    obsForm2_flip_img = pygame.transform.scale(obsForm_flip, (41, obsForm2_locate_y-100))  #cột trên
    obsForm2_flip = form.blit(obsForm2_flip_img, (obsForm2_locate_x, 0))
    obsForm2_locate_x -= obsForm_move  #di chuyển obs2 sang trái

    #chướng ngại vật 3
    obsForm3 = pygame.transform.scale(obsForm, (41,obsForm3_locate_y))      #cột dưới
    obsForm3 = form.blit(obsForm, (obsForm3_locate_x, obsForm3_locate_y))

    obsForm3_flip_img = pygame.transform.scale(obsForm_flip, (41, obsForm3_locate_y-100)) #cột trên
    obsForm3_flip = form.blit(obsForm3_flip_img, (obsForm3_locate_x, 0))
    obsForm3_locate_x -= obsForm_move  #di chuyển obs3 sang trái

    #tạo chướng ngại vật mới
    if  obsForm1_locate_x<-41:
        obsForm1_locate_x = 601
        obsForm1_locate_y = random.randint(250, 450)
        obsForm1_pass = False
    if  obsForm2_locate_x<-41:
        obsForm2_locate_x = 601
        obsForm2_locate_y = random.randint(250, 450)
        obsForm2_pass = False
    if  obsForm3_locate_x<-41:
        obsForm3_locate_x = 601
        obsForm3_locate_y = random.randint(250, 450)
        obsForm3_pass = False
    

    if check:   #nếu ko có va chạm thì trò chơi tiếp tục tải lên form
        #chim
        birdMovement += g
        birdRectangle.centery += birdMovement   #hiệu ứng chim bị rớt xuống dưới
        rotatedBird = rotateBird(bird)
        form.blit(rotatedBird, birdRectangle)  #tải hình ảnh chim lên form
        check = collisionHanding(listOfObs)     #kiểm tra va chạm

        #hiển thị tính điểm, nếu ko va chạm và qua 1 cột thì điểm tăng 1
        if obsForm1_locate_x < birdRectangle.centerx and obsForm1_pass == False:
            score+=1
            obsForm1_pass = True
            scoreSound.play()
        if obsForm2_locate_x < birdRectangle.centerx and obsForm2_pass == False:
            score+=1
            obsForm2_pass = True
            scoreSound.play()
        if obsForm3_locate_x < birdRectangle.centerx and obsForm3_pass == False:
            score+=1
            obsForm3_pass = True
            scoreSound.play()

        #Kiểm tra va chạm
        listOfObs = [obsForm1, obsForm1_flip, obsForm2, obsForm2_flip, obsForm3, obsForm3_flip]
        for obs in listOfObs:
            if birdRectangle.colliderect(obs):
                obsForm_move = 0

        #hiển thị điểm đang ghi được
        show_score('running')
    else:
        form.blit(gameOver, gameOverRectangle)
        highest_score = updateScore(score, highest_score)
        show_score('game over')
    #kiểm tra sự di chuyển của sàn
    if check:   #nếu ko va chạm với cột thì sàn vẫn di chuyển
        floorMove -= 2      #sàn sẽ di chuyển lùi khi bird tiến lên -> sẽ sửa lại form.blit(floor, (0,550))
        newFloor()
        if floorMove == -400:
            floorMove = 0       #đặt sàn 1 ra ngay sau sàn 2 khi sàn 1 di chuyển hết
    else:   #nếu va chạm với cột thì dừng di chuyển
        floorMove -= 0
        newFloor()
    pygame.display.update()     #cập nhật các thay đổi để hiển thị 
    fps.tick(60)    #set fps = 60