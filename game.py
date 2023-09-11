from direct.showbase.ShowBase import ShowBase
from panda3d.core import OrthographicLens
from panda3d.core import Vec4, Vec3
from direct.task import Task 
import simplepbr

class Game(ShowBase):

    def __init__(self):
        super().__init__()
        simplepbr.init()

        self.ground = loader.loadModel("art/ground.glb")
        self.ground.reparentTo(base.render)
        self.ground.setScale(2.6)
        # apply auto shader to groound
        self.ground.setShaderAuto()

        self.player = loader.loadModel("art/player.glb")
        self.player.reparentTo(base.render)
        self.player.setZ(0.5)
        #player variables
        self.speed = 10.0
        self.velocity = Vec3() # we only care about x coord and y coord

        self.keys = {
            "move_right" : False,
            "move_left" : False,
            "move_up" : False,
            "move_down" : False,
        }

        self.accept("d", self.update_key, ["move_right", True])
        self.accept("d-up", self.update_key, ["move_right", False])
        self.accept("a", self.update_key, ["move_left", True])
        self.accept("a-up", self.update_key, ["move_left", False])
        self.accept("s", self.update_key, ["move_down", True])
        self.accept("s-up", self.update_key, ["move_down", False])
        self.accept("w", self.update_key, ["move_up", True])
        self.accept("w-up", self.update_key, ["move_up", False])

        #set camera lens to orthographic
        lens = OrthographicLens()
        lens.setFilmSize(30, 20)
        base.cam.node().setLens(lens)

        base.cam.setPos(0, -25, 45)
        base.cam.setP(-60)

        taskMgr.add(self.move_player, "move_player")

    def move_player(self, task):
        dt = globalClock.get_dt()
        #print(dt)
        direction = Vec3()

        if self.keys["move_right"]:
            direction.x += 1
        if self.keys["move_left"]:
            direction.x -= 1
        if self.keys["move_down"]:
            direction.y -= 1
        if self.keys["move_up"]:
            direction.y += 1

        direction = direction.normalized()
        if direction != Vec3():
            self.player.look_at(self.player.getPos() + direction)
        
        self.velocity = direction * self.speed * dt
        self.player.setPos(self.player.getPos() + self.velocity)
        
        

        print(self.velocity)
        return task.cont
    
    def update_key(self, action , state):
        self.keys[action] = state

        
game = Game()
game.run()