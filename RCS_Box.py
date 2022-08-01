import numpy as np
import re

class RCS_box:
    def __init__(self, path, outpath, config_path, scale):
        self.path = path                            #The path of the obj file you want to process
        self.scale = scale                          #The scale of killer box
        self.outpath = outpath
        self.config_path = config_path
        print(self.outpath)
        self.face_default = ["f 3//3 2//2 1//1\n",
                             "f 2//2 3//3 4//4\n",
                             "f 5//5 3//3 1//1\n",   
                             "f 3//3 5//5 7//7\n",
                             "f 2//2 5//5 1//1\n",
                             "f 5//5 2//2 6//6\n",
                             "f 7//7 6//6 8//8\n",
                             "f 6//6 7//7 5//5\n",
                             "f 4//4 7//7 8//8\n",
                             "f 7//7 4//4 3//3\n",
                             "f 6//6 4//4 8//8\n",
                             "f 4//4 6//6 2//2\n"      
                                ]

    #Start function
    def start(self):
        f = open(self.path,"r")                     #read OBJ file
        np_file = np.array(f.readlines())

        delete_line = np.where(np.char.find(np_file,'#')>-1)        #remove comments
        #######################                                                                
        #sometimes, obj file have color parameters with "#" in line, we need to ignore it.
        for i in delete_line[0]:
            if(np_file[i][0] == 'v'):
                delete_line = np.delete(delete_line,np.where(delete_line == i))
        np_file = np.delete(np_file,delete_line)
        ######################

        new_file = open(self.outpath, "w")          #Output OBJ file
        
        face_line = np_file[np.where(np.char.find(np_file,'f ')>-1)]            #Get all face lines
        v_line = np_file[np.where(np.char.find(np_file,'v ')>-1)]               #Get all vertex lines
        vn_line = np_file[np.where(np.char.find(np_file,'vn ')>-1)]             #Get all vertex normals 
        self.vertex_process(v_line, vn_line, new_file)                          #Process and write verties and vertex normals
        self.face_process(face_line, new_file)                                  #Process and write faces.
        new_file.close()
        
    
    #vertex processing function
    def vertex_process(self, v_line, vn_line, new_file):
        np_vline = np.char.split(v_line)                                        
        np_vline = np_vline.tolist()
        #######################################
        #solve the problem "#" can not be transfered to np array
        new_np_vline = []
        for np_v in np_vline:
            new_np_vline.append(np_v[1:4])
        #######################################
        np_vline = np.array(new_np_vline)

        np_vline = np_vline.astype(float)
        x = self.box_offset(np_vline[:,0].min(), np_vline[:,0].max(), self.scale)
        y = self.box_offset(np_vline[:,1].min(), np_vline[:,1].max(), self.scale)
        z = self.box_offset(np_vline[:,2].min(), np_vline[:,2].max(), self.scale)

        config_data = self.read_config(self.config_path)                       #reading config data and comparing the recive point with model

        new_x = [min(x + config_data[0]), max(x + config_data[0])]             
        new_y = [min(y + config_data[1]), max(y + config_data[1])]      
        new_z = [min(z + config_data[2]), max(z + config_data[2])]

        normal = [-1.570796,1.570796]

        i = 0
        while(i<8):
            
            x_l = i%2                                                           #The first bits of 3 bits binary counter
            y_l = (i//2)%2                                                      #The second bits of 3 bits binary counter
            z_l = (i//4)%2                                                      #The third bits of 3 bits binary counter
            new_file.write(f"vn {normal[x_l]} {normal[y_l]} {normal[z_l]}\nv {new_x[x_l]} {new_y[y_l]} {new_z[z_l]}\n")     #create a RCS box
            i += 1
        for i in range(len(v_line)):                                           #Write down original model information
            new_file.write(vn_line[i])
            new_file.write(v_line[i])

    #face processing function
    def face_process(self, face_line, new_file):
        np_faces = np.char.split(face_line)
        np_faces = np_faces.tolist()

        if(np_faces[1][1].find("//") != -1):                                     #Process format: f 1//1 2//2 3//3
            new_np_face = []
            for i in np_faces:
                new_line = []
                for j in i[1:]:
                    new_line.append(j.split("//")[0])
                new_np_face.append(new_line)

            for i in self.face_default:                                         #create a RCS box
                new_file.write(i)


            for i in new_np_face:                                           #Write down original model information
                new_string = 'f'
                for j in i:
                    new_string += f' {int(j)+8}//{int(j)+8}'
                new_string += "\n"
                new_file.write(new_string)

        else:                                                                   #Process format: f 1 2 3
            for i in self.face_default:                                         #create a RCS box
                new_file.write(i)

            for i in np_faces[1:]:
                new_string = 'f'
                for j in i:
                    new_string += f' {int(j)+8}'                                           #Write down original model information
                new_string += "\n"
                new_file.write(new_string) 

    #remove offset function
    def box_offset(self, min, max, scale):
        offset = (max - min)/2
        mid = (max + min)/2
        final_list = [mid-offset*scale, mid+offset*scale]
        return final_list
    
    #config file processing
    def read_config(self,config_path):
        f = open(config_path,'r')
        lines = f.readlines()
        
        #get shpere_x,_y,_z
        origin = []
        origin_line = [match for match in lines if "sphere" in match]
        for i in origin_line:
            origin.append(int(re.sub( "\D" , "", i)))

        #get d_x,_y,_z
        detail = []
        for i in lines:
            judge = re.match('^d',i)
            if judge:
                detail.append(int(re.sub( "\D" , "", i)))
        f.close()

        #generate recive length
        final_list = []
        for i in range(3):
            temp = detail[i] + origin[i]
            mid = (temp + origin[i])/2
            offset = (temp - origin[i])/2
            final_list.append([mid-offset*2, mid+offset*2])

            print(final_list)
        return final_list







