try:
  import numpy as np
  import os, sys
  import cv2
  import keyboard
  import shutil
  import discord_webhook
  from discord_webhook import DiscordWebhook, DiscordEmbed
  from helper import functions as funcs
except ModuleNotFoundError as e:
  print(f'ERROR: An error occurred when importing dependencies. \n{e}\n')
  sys.exit(1)


class LocalHelper:

  def sendDiscordAlert(file_path):
    embed = DiscordEmbed()
    file_name = file_path.split('/')[-1]

    embed.set_title('Scout Alert')
    embed.set_description(f'Scout detected a face: {funcs.getTime()}')
    with open(file_path, 'rb') as f:
      file_data = f.read()

    webhook.add_file(file_data, file_name)
    webhook.add_embed(embed)
    response = webhook.execute()
    return response
  
  def zipFiles(output, target_files):
    dump_dir = f'dump: {funcs.getTime()}'
    os.mkdir(dump_dir)
    for target in target_files:
      with open(target, 'rb') as Fin:
        content = Fin.read()
      with open(f'{dump_dir}/{target}', 'wb') as Fout:
        Fout.write(content)
        
    zip_file = shutil.make_archive(output, 'zip', dump_dir)
    


# TODO's
'''
* Make it send a 'F15' input so we dont go to sleep
* Create a cap on amount of snapshots
* Snapshot every time a face is detected and save it !
* Output video file
'''

webhook_url = 'https://discord.com/api/webhooks/1140680728519127092/9_a9xGQKaE59MiyY8r8SkaA6RwceDBYXlFe6eW8NqEtr0hoBJzaNyqRfJ7_SDtIkrWz1'
faceCascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
webhook = DiscordWebhook(url=webhook_url)
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # set Width
cap.set(4, 480)  # set Height

while True:
  ret, img = cap.read()
  img = cv2.flip(img, 1)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.2,
    minNeighbors=5,
    minSize=(20, 20)
  )

  for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = img[y:y + h, x:x + w]

  if str(faces) == '()':
    print('No faces')
  else:
    print(f'Face found: {funcs.getTime()}')
    snapshot_file = f'facedump/{funcs.uniqueIDGen()}.png'
    cv2.imwrite(snapshot_file, img)
    #LocalHelper.sendDiscordAlert(snapshot_file)

  if len(os.listdir('facedump')) >= 50:
    print('OVERFLOW')

  cv2.imshow('video', img)
  key = cv2.waitKey(30) & 0xff
  if key == 27:  # press 'ESC' to quit
    break

cap.release()
cv2.destroyAllWindows()
