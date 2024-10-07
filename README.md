Workflow new folder

Buat folder di www
Pake git bash cd ke folder tersebut (cd path)
git clone https://github.com/GeryYulianto/SeniorExperts
Workflow push git

pastiin udah di folder hasil clone (cd yourpath/SeniorExperts)
git pull origin main (buat pastiin file kamu yang terupdate)
Bikin branch baru (git checkout -b name-branch)
git push origin new-branch
git add .
git commit -m "Your message"
git push origin new-branch
git checkout main (balik ke branch main)
git merge new-branch (merge dengan branch yang barusan kamu buat)
Workflow push git simple (kalo dikit filenya)

git pull origin main
modify filenya
git status (cek kalo beneran dianggep modify gak sama git)
git add .
git commit -m "text"
git push origin main
