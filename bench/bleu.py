from nltk.translate.bleu_score import sentence_bleu
from nltk import word_tokenize
import pandas as pd

# 候选作文（学生作文原文，保留所有占位符和错误）
all_candidates = pd.read_csv("/Users/ylm/THU/code/exp/data/random_essays_50.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')



# 参考作文（假设的标准答案）
reference_text = ["","","","","","","","",""]
reference = [[] for _ in range(9)]
reference_text[1]="""
Dear @ORGANIZATION1, The computer blinked to life and an image of a blonde haired girl filled the screen. It was easy to find out how life was in @LOCATION2, thanks to the actual @CAPS1 girl explaining it. Going to the library wouldn't have filled one with this priceless information and human interection. Computers are a nessessity of life if soceity wishes to grow and expand. They should be supported because they teach hand eye coordination, give people the ability to learn about faraway places, and allow people to talk to others online. Firstly, computers help teach hand eye coordination. Hand-eye coordination is a useful ability that is usod to excel in sports. In a recent survey, @PERCENT1 of kids felt their hand eye coordination improves after computer use. Even a simple thing like tying can build up this skill. Famous neurologist @CAPS2 @PERSON1 stated in an article last week that, ""@CAPS3 and computer strength the @CAPS2. When on the computer, you automatically process what the eyes see into a command for your hands."" @CAPS4 hand eye coordination can improve people in sports such as baseball and basketball. If someone wan't to become better in these sports, all they'd need to do was turn on the computer. Once people become better at sports, they're more likely to play them and become more healthy. In reality, computers can help with exercising instead of decreasing it. Additionaly, computers allow people to access information about faraway places and people. If someone wanted to reasearch @LOCATION1, all they'd need to do was type in a search would be presented to them in it would link forever to search through countless things. Also, having the ability to learn about cultures can make peole peole and their cultures, they understand others something. Increase tolerance people are. Computers are a resourceful tool that they can help people in every different aspect of life. Lastly, computer and in technology can allow people to chat. Computer chat and video chat can help the all different nations. Bring on good terms places other than can help us understand story comes out about something that happend in @LOCATION3, people can just go on their computer and ask an actual @LOCATION3 citizen their take on the matter. Also, video chat and online conversation can cut down on expensive phone bills. No one wants to pay more than they have to in this economy. Another good point is that you can acess family members you scaresly visit. It can help you connect within your own family more. Oviously, computers are a useful aid in todays era. their advancements push the world foreward to a better place. Computers can help people because they help teach handeye coordination, give people the bility to learn about faraway places and people, and allow people to talk online with others. Think of a world with no computers or technologicall advancements. The world would be sectored and unified, contact between people scare, and information even. The internet is like thousands or librarys put together. Nobody would know much about other nations and news would travel slower. Is that the kind of palce you want people to live in?
"""
reference[1] = [word_tokenize(reference_text[1].lower())]

reference_text[2]="""
What is freedom of speech? It is the ability to speak out your mind without fear of prosecution – but is that all it is? Is it limited to verbal opinion? Or does every kind of speech count? Do books, music, movies, magazine, newspaper articles, and cartoons come under “speech”? Or are they the targets of the arrow called censorship? Author Katherine Paterson said, “if I have the right to remove that book from the shelf…then you also have exactly the same right and so does everyone else. And then we have no books left on the shelf for any of us.” Opinions can be expressed in several different ways. Vocally expressing one’s views cannot be repressed for once the words are spoken, they cannot be taken back. Books can be retracted; music can be banned; movies can be halted – but how are they any different from verbal expression? Merely because they express points of view through art does not mean that they are not a form of “speech” on the author or musician or film maker’s part. They are his or her way of bringing personal ideas and opinions to the public in an engaging manner, providing entertainment and broadening horizons simultaneously. Libraries everywhere have banned countless works under the pretext of their “offensive” nature. J.D. Salinger’s literary masterpiece, The Catcher in the Rye, was the cause of numerous revolts across the nation – parents did not want their children reading it in school, educators were appalled by the gross and perverted aspects of the novel – but today, people describe it as a book that captured the mindset of the youth of America during the 40s perfectly and a story that is “truly American.” What if, 60 years ago, censorship had engulfed the tale of Holden Caulfield forever? What if his story had been burned and doomed to never see the light of the day again? Would America have lost a great novel because of how it “offended” some people? Yes, they would have. Censorship is not “bad.” Sometimes, it is necessary. For example, sorting movies according to what age someone can watch them without it being “inappropriate” is beneficial it helps you receive knowledge and the truth about the world when you are truly ready to comprehend it. But banning them because of certain aspects that may not be pleasant to some is not helping anyone. If you do not want your child to read a book you deem “inflammatory,” make it your personal rule to keep them away from it. Libraries can make a different section of those kind of works, require parental consent to gain acces to them, or put a warning on them, but not stifle the creative souls of the minds behind these works. Paterson is right. One person may have a problem with a certain book – he raises people against it – the book is banned. Another woman may not like a song because of negative ideas – she rounds up other critics – the song is banned. A parent may find a certain movie inappropriate and offensive – he creates petitions banning it – Page 10 of 32 the movie is banned. You will never find them in any library anywhere. The idea here is that everyone will have problems with something or the other, but if we start getting rid of those things we ultimately end up with nothing at all. Control, not censor. Do not destroy others opinions based on yours. They may be attacking yours, but by censoring them, you are doing the same thing.
"""
reference[2] = [word_tokenize(reference_text[2].lower())]

reference_text[7]="""
If all started a few Christmas ago, I am not sure how long ago it was, but I have to say it was a few years ago. You see, my family has this rule that we are not allowed to open presents in seven o'clock. This rule is easy to uphold, usually, though instead of working up at my normal six-thirty, I wrote up and it was four-fifteen! Just like any little kid on Christmas, my first thought was to sneak down stairs and try to figure out what was to my presents. I knew better enough, I knew that if I was to sneak down to try to figure out my presents I would get to trouble. That was not how I wanted to spend my Christmas, so I decided to read, play with toys, and color to pass the time.        The minutes went by more to fast, Every minute felt like a hour, every hour felt like a decade! It reminded me of those movies where time would slow down and sometimes even stop.        As time wore on, the thought to sneak and take a peek at my presents sounded ever more speaking, several more minutes were by...at least moment. I decided enough was enough too, I did something that I would regret later. I snuck down stairs! It was not hard. In seconds I was at the Christmas tree I went to go on my first present when suddenly I ascertainfully hit a big present that made a loud noise! Emmediately my mom awoke to find me, too worried! As a result to my actions, my family was not allowed to open presents. If eight o'clock! It makes me now know that when someone is not patient, it is like they are asking selfish or only thinking about themselves. Now I know it means to be patient, thinking back marks me, believe that if I would have been patient enough to work in seven o'clock, I would have been able to open my Christmas presents taster.
"""
reference[7] = [word_tokenize(reference_text[7].lower())]

reference_text[8]="""
All people, no matter what age, want to be accepted in life. Sometimes, however, we think illogically and make bad decisions. To be accepted is to have a place in the sun among your peers, and some people will do whatever it takes to get there. When my friend Jordan tried to get his place in the sun, he expected to get blisters, but he didn’t expect to lose his life.   Lost River is a recreation spot out in the middle of nowhere. My friend Jordan and I were on a day trip with a group of other boys. Jordan was really trying to fit in. I couldn’t really understand what his motivation was or why fitting in with these boys was so important. I just wanted to have some fun with my friend, but I might as well have been on the moon.   We were sitting at the picnic table when Martin, the oldest of the boys, spoke:  “How about we go to the top of the bridge?”   I laughed, but Jordan jumped right up and said, “Sure, let’s go.” I was astonished—Jordan hated to swim, and the only reason people went up there was to jump off into the water.   I was screaming at them saying this was a stupid idea, but Jordan would do anything to be part of the crowd. As we approached the gargantuan, rusted bridge, I started to shiver. It must have been over a hundred feet high. I trembled as we walked to the center. It was illegal to do this, so I was trying to get them to stop.   “Who’s going first?” asked Martin. The boys turned to Jordan. “Jordan, you go first.”   “I don’t know, it looks pretty high,” Jordan said. I pleaded with him, shaking my head trying to get him to turn back.   “Go! Go! Go! Go!” chanted the boys.   “Jordan, let’s just go back!” I screamed.   “Shut up!” Jordan gave in. He climbed over the rail cautiously. I tried to grab him, but the boys held me back.   “Here I go!” he said.   Then he jumped.   We gasped and ran to the edge. There was an eerie silence as his body fell farther and farther. When the splash came, the boys stopped chanting. My eyes were glued to the water—30 seconds, 5 minutes. We froze, unable to see Jordan. Martin ran for help as I sank down. I knew I wouldn’t see him again.   It took an hour for the ambulance to arrive. His body wasn’t recovered for another four. They said his neck broke on impact. Why did he do it? Why didn’t I stop him?   To this day, I ask myself those questions. Why was being accepted so important? Every time I visit his grave, I wonder. The headstone reads:  JORDAN THOMAS MARSEN  1987–2009  JUST 30   Jordan wasn’t the only one left with blisters after trying to find his place in the sun. His parents, friends, and I got blisters too. If it takes all of this to have a place in the sun, I’d choose rain any day.
"""
reference[8] = [word_tokenize(reference_text[8].lower())]

results = []
# 遍历dataframe中的每一行
for index, candidate in all_candidates.iterrows():
    candidate_text = candidate.loc["essay"]
    essay_set = candidate.loc["essay_set"]
    essay_id = candidate.loc["essay_id"]
    # 直接分词（不处理占位符、不分句、不清理）
    candidate = word_tokenize(candidate_text.lower())  # 统一小写

    # 计算BLEU-1（仅1-gram权重）
    bleu1_score = sentence_bleu(reference[essay_set], candidate, weights=(1, 0, 0, 0))
    # 计算BLEU-2（1-gram和2-gram权重）
    bleu2_score = sentence_bleu(reference[essay_set], candidate, weights=(0.5, 0.5, 0, 0))
    # 计算BLEU-4（1-gram、2-gram、3-gram和4-gram权重）
    bleu4_score = sentence_bleu(reference[essay_set], candidate, weights=(0.25, 0.25, 0.25, 0.25))

    results.append({
            "essay_id": essay_id,
            "bleu1_score": bleu1_score,
            "bleu2_score": bleu2_score,
            "bleu4_score": bleu4_score,
        })



# 转换为DataFrame
results_df = pd.DataFrame(results)

# 按需设置列顺序
final_df = results_df[["essay_id", "bleu1_score", "bleu2_score", "bleu4_score"]]

# 保存结果
final_df.to_csv("/Users/ylm/THU/code/exp/data/bleu_scores.csv", sep='\t', index=False)
