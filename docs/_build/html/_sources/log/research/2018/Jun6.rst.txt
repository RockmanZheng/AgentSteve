Wed 6 Jun 2018
==============

Getting Started With Python
---------------------------
In order to import module ``MalmoPython``, you will need to find the shared library *Python_Examples/MalmoPython.so* under Malmo project and copy it to your Python's site package location(s), which can be checked by running

``import site;site.getsitepackages()``

If you are going to use ``malmoutils`` as well, please also copy the file *Python_Examples/malmoutils.py* to your site package directory.

Windows Support
---------------
Malmo seems to be not supporting Windows system very well yet. In fact, it seems that Minecraft mod development on Linux is the main stream. For more information, check *Minecraft Coder Pack*, and `Minecraft Forge <http://files.minecraftforge.net/>`_. 

Remark: Malmo project is built upon Minecrft Forge.

Video Recording
---------------
First you can check *Research/explore_experiments/001/script01.py*. 

I used ``VideoProducer`` to specify output frames to be the size of 256x256. And use the API ``MalmoPython.MissionRecordSpec.recordMP4`` to specify we want to record video into MP4 format.

Run *script01.py* with arguments as:

.. code-block:: shell

    python script01.py --record_video --recording_dir=mission_records

The first argument ``record_video`` tells Malmo to record video. The second argument ``recording_dir`` specify in which directory we store our records. While running mission, Malmo will temporarily store all records including video records under a folder named ``mission_records``. After the mission is completed, Malmo will compress all the records and store it to destination specified by API ``MalmoPython.MissionRecordSpec.setDestination``. In *script01.py* we set destination to be *mission_records/Mission_1.tgz*.

After a mission is completed, we decompress *mission_records/Mission_1.tgz* and play video record to review the mission.

We discovered that in first person view, the hotbar slots and hands of our agent **did not** get recorded into video. So we may need to allow the agent to observe the game in third person view to better let it understand the world.


