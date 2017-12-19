# -*- coding: utf-8 -*-

import mitsuba as mit
import mitsubaToPBRT as mtpbrt
import classes as directives
import numpy as np

def pbrt_writeParams(paramList, dictionary):
    s = ''
    for param in paramList:
        if param.name in dictionary:
            pbrt_param = dictionary[param.name]
            s = s + '"' + param.val_type + ' ' + pbrt_param + '" '
            if param.val_type is 'string' or param.val_type is 'bool':
                s = s + '[ "' + param.value + '" ] '
            else:
                s = s + '[ ' + param.value + ' ] '
                
    return s

def pbrt_shapeString(shape, numberOfTabs):
    autoTab = '\t'
    s = ''
    
    if shape.type == 'obj' or shape.type == 'ply':
        s = s + (autoTab * numberOfTabs) + 'Shape "plymesh" "string filename" [ "' + shape.getFile + '" ]\n'
            
    elif shape.type == 'cube':
        # cube will be a triangle mesh (god help me)
        points = []
        
        points.append(np.sum(shape.transform.matrix * np.array([-1, -1, -1, 1]), axis = 1))
	    points.append(np.sum(shape.transform.matrix * np.array([-1, 1, 1, 1]), axis = 1))
	    points.append(np.sum(shape.transform.matrix * np.array([1, 1, -1, 1]), axis = 1))
	    points.append(np.sum(shape.transform.matrix * np.array([1, -1, 1, 1]), axis = 1))
        points.append(np.sum(shape.transform.matrix * np.array([-1, 1, -1, 1]), axis = 1))
        points.append(np.sum(shape.transform.matrix * np.array([-1, -1, 1, 1]), axis = 1))
        points.append(np.sum(shape.transform.matrix * np.array([1, -1, -1, 1]), axis = 1))
        points.append(np.sum(shape.transform.matrix * np.array([1, 1, 1, 1]), axis = 1))
        
        points.append(points[5]), points.append(points[0]), points.append(points[3]), points.append(points[6]) # 8, 9, 10, 11
        points.append(points[7]), points.append(points[2]), points.append(points[1]), points.append(points[4]) # 12, 13, 14, 15
        points.append(points[4]), points.append(points[1]), points.append(points[0]), points.append(points[5]) # 16, 17, 18, 19
        points.append(points[6]), points.append(points[3]), points.append(points[2]), points.append(points[7]) # 20, 21, 22, 23
                
        s = s + (autoTab * numberOfTabs) + 'Shape "trianglemesh" '
        s = s + '"integer indices" [ 0 2 1 0 3 2 4 6 5 4 7 6 8 10 9 8 11 10 12 14 13 12 15 14 16 18 17 16 19 18 20 22 21 20 23 22 ] "point P" [ '
        
        for i in range(0, 24):
            s = s + str(points[i][0] + ' ' + str(points[i][1]) + ' ' + str(points[i][2]) + ' '
    
        s = s + '] '        
       
        #normal for all 4 points in a face are the same
        # faces: 1 = 0 1 2 3; 2 = 4 5 6 7; 3 = 8 9 10 11; 4 = 12 13 14 15; 5 = 16 17 18 19; 6 = 20 21 22 23;
        normalFace1 = np.cross(points[2] - points[0], points[3] - points[1])
        normalFace2 = np.cross(points[6] - points[4], points[7] - points[5])
        normalFace3 = np.cross(points[10] - points[8], points[11] - points[9])
        normalFace4 = np.cross(points[14] - points[12], points[15] - points[13])
        normalFace5 = np.cross(points[18] - points[16], points[19] - points[17])
        normalFace6 = np.cross(points[22] - points[20], points[23] - points[21])
        
        s = s + '"normal N" [ '
        for i in range(0, 4):
            s = s + str(normalFace1[0] + ' ' + str(normalFace1[1]) + ' ' + str(normalFace1[2]) + ' '
        for i in range(0, 4):
            s = s + str(normalFace2[0] + ' ' + str(normalFace2[1]) + ' ' + str(normalFace2[2]) + ' '
        for i in range(0, 4):
            s = s + str(normalFace3[0] + ' ' + str(normalFace3[1]) + ' ' + str(normalFace3[2]) + ' '
        for i in range(0, 4):
            s = s + str(normalFace4[0] + ' ' + str(normalFace4[1]) + ' ' + str(normalFace4[2]) + ' '
        for i in range(0, 4):
            s = s + str(normalFace5[0] + ' ' + str(normalFace5[1]) + ' ' + str(normalFace5[2]) + ' '
        for i in range(0, 4):
            s = s + str(normalFace6[0] + ' ' + str(normalFace6[1]) + ' ' + str(normalFace6[2]) + ' '
        
        s = s + '] '
        
        # default uv
        s = s + '"float uv" [ 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 ]\n'
            
    elif shape.type == 'sphere':
        s = s + (autoTab * numberOfTabs) + 'TransformBegin\n'
        s = s + (autoTab * (numberOfTabs + 1)) + 'Transform [ 1 0 0 0 0 1 0 0 0 0 1 0 ' + str(shape.center[0]) + ' ' + str(shape.center[1]) + ' ' + str(shape.center[2]) + ' ' + ' 1 ]\n'
        s = s + (autoTab * (numberOfTabs + 1)) 'Shape "sphere" '
        s = s + pbrt_writeParams(shape.params, mtpbrt.shapeParam)
        s = s + '\n'
        s = s + (autoTab * numberOfTabs) + 'TransformEnd\n'
        
    elif shape.type == 'cylinder':
        pass
        
    elif shape.type == 'rectangle':
        # rectangle will be a triangle mesh
        p0 = np.sum(shape.transform.matrix * np.array([-1, -1, 0, 1]), axis = 1)
        p1 = np.sum(shape.transform.matrix * np.array([1, -1, 0, 1]), axis = 1)
        p2 = np.sum(shape.transform.matrix * np.array([1, 1, 0, 1]), axis = 1)
        p3 = np.sum(shape.transform.matrix * np.array([-1, 1, 0, 1]), axis = 1)        

        s = s + (autoTab * numberOfTabs) + 'Shape "trianglemesh" "integer indices" [ 0 1 2 0 2 3 ] "point P" '
        s = s + '[ ' + str(p0[0]) + ' ' + str(p0[1]) + ' ' + str(p0[2]) + ' '
        s = s + str(p1[0]) + ' ' + str(p1[1]) + ' ' + str(p1[2]) + ' '
        s = s + str(p2[0]) + ' ' + str(p2[1]) + ' ' + str(p2[2]) + ' '
        s = s + str(p3[0]) + ' ' + str(p3[1]) + ' ' + str(p3[2]) + ' ] '
                
        # normal for all 4 points in a rectangle is the same as face normal
        normal = np.cross(p2 - p0, p3 - p1)
        s = s + '"normal N" ['
        for i in range(0,4):
            s = s + str(normal[0] + ' ' + str(normal[1]) + ' ' + str(normal[2]) + ' '

        # default uv
        s = s + '"float uv" [ 0 0 1 0 1 1 0 1 ]\n'
            
    elif shape.type == 'disk':
        pass
            
    elif shape.type == 'hair':
        pass
                        
    if s.
                        
    if s.material is not None:
        s = s + 'Material "'
                        
        if isinstance(s.material, directives.AdapterMaterial):
            # convert material type
                        
            s = s + '" '
            params = pbrt_writeParams(s.material.material.params, mtpbrt.materialParam)
            s = s + params + '\n'
                        
                        
        elif is instance(s.material, directives.Material):
            # convert material type
                        
            s = s + '" '
            params = pbrt_writeParams(s.material.params, mtpbrt.materialParam)
            s = s + params + '\n'
                
    return s


def toPBRT(scene):
    np.set_printoptions(suppress=True)
    textures = {} # texture dictionary. entries are 'material_name' : 'texture_id'
    
    with open("scene.pbrt", 'w') as outfile:
        # scene directives
        # integrator
        if scene.integrator:
            outfile.write('Integrator ')

            if scene.integrator.int_type in mtpbrt.integratorType:
                int_type = mtpbrt.integratorType[scene.integrator.int_type]
                outfile.write('"' + int_type + '" ')
            else:
                outfile.write('"path" ')

            p = pbrt_writeParams(scene.integrator.params, mtpbrt.integratorParam)
            outfile.write(p + '\n')

        # transform
        if scene.sensor.transform.matrix:
            outfile.write('Transform ')
            outfile.write('[ ')

            # convert transform matrix to inverse transpose (PBRT default)
            m = scene.sensor.transform.matrix
            m_T = np.transpose(m)
            m_IT = np.linalg.inv(m_T)

            for i in range(0,4):
                for j in range(0,4):
                    outfile.write(str(m_IT[i][j]))
                    outfile.write(' ')

            outfile.write(']')
            outfile.write('\n')

        # sampler
        if scene.sensor.sampler:
            outfile.write('Sampler ')

            if scene.sensor.sampler.sampler_type in mtpbrt.samplerType:
                sampler_type = mtpbrt.samplerType[scene.sensor.sampler.sampler_type]
                outfile.write('"' + sampler_type + '" ')
            else:
                outfile.write('"sobol" ')

            p = pbrt_writeParams(scene.sensor.sampler.params, mtpbrt.samplerParam)
            outfile.write(p + '\n')

        # filter
        if scene.sensor.film.filter_type:
            outfile.write('PixelFilter ')

            if scene.sensor.film.filter_type in mtpbrt.filterType:
                filter_type = mtpbrt.filterType[scene.sensor.film.filter_type]
                outfile.write('"' + filter_type + '" ')
            else:
                outfile.write('"triangle" ')
    
            outfile.write('\n')

        # film
        if scene.sensor.film:
            outfile.write('Film ')

            if scene.sensor.film.film_type in mtpbrt.filmType:
                film_type = mtpbrt.filmType[scene.sensor.film.film_type]
                outfile.write('"' + film_type + '" ')
            else:
                outfile.write('"image" ')

            p = pbrt_writeParams(scene.sensor.film.params, mtpbrt.filmParam)
            outfile.write(p + '\n')

        # sensor/camera
        if scene.sensor:
            outfile.write('Camera ')

            if scene.sensor.sensor_type in mtpbrt.sensorType:
                sensor_type = mtpbrt.sensorType[scene.sensor.sensor_type]
                outfile.write('"' + sensor_type + '" ')
            else:
                outfile.write('"perspective" ')

            p = pbrt_writeParams(scene.sensor.params, mtpbrt.sensorParam)
            outfile.write(p + '\n')

        # scene description
        outfile.write('WorldBegin\n')
        
        # texture declaration
        tex_count = 1
        
        for material in scene.materials:
            # case bumpmap: texture with adapter texture
            if isinstance(material, directives.BumpMap):
                tex = material.texture
                
                if tex is not None:
                    id = 'Texture' + str(tex_count).zfill(2)
                    textures[material.adapter.mat_id] = id
                
                    # outer texture for bumpmap is float. otherwise, spectrum
                    outfile.write('Texture "' + id + '" "float" ')
                
                    if tex.tex_type == 'bitmap':
                        outfile.write('"imagemap" ')
                    else:
                        if tex.tex_type in mtpbrt.textureType:
                            tex_type = mtpbrt.textureType[tex.tex_type]
                            outfile.write('"' + tex_type + '" ')
                
                    for param in tex.params:
                        if param.name == 'filename':
                            outfile.write('"string filename" [ "' + param.value + '" ] ')
                        elif param.name == 'filterType':
                            if param.value == 'ewa':
                                outfile.write('"bool trilinear" [ "false" ] ')
                            else:
                                outfile.write('"bool trilinear" [ "true" ] ')
                        else:
                            # search the dictionary
                            p = pbrt_writeParams(shape.params, mtpbrt.textureParam)
                            outfile.write(p + '\n')
        
    
                    tex_count += 1
                    outfile.write('\n')
        
            # case adapter: texture in adapter -> material
            elif isinstance(material, directives.AdapterMaterial):
                tex = material.material.texture
                
                if tex is not None:
                    id = 'Texture' + str(tex_count).zfill(2)
                    textures[material.mat_id] = id
                
                    outfile.write('Texture "' + id + '" "spectrum" ')
                    
                    if tex.tex_type == 'bitmap':
                        outfile.write('"imagemap" ')
                    else:
                        if tex.tex_type in mtpbrt.textureType:
                            tex_type = mtpbrt.textureType[tex.tex_type]
                            outfile.write('"' + tex_type + '" ')

                    for param in tex.params:
                        if param.name == 'filename':
                            outfile.write('"string filename" [ "' + param.value + '" ] ')
                        elif param.name == 'filterType':
                            if param.value == 'ewa':
                                outfile.write('"bool trilinear" [ "false" ] ')
                            else:
                                outfile.write('"bool trilinear" [ "true" ] ')
                        else:
                            # search the dictionary
                            p = pbrt_writeParams(shape.params, mtpbrt.textureParam)
                            outfile.write(p + '\n')
        
                    tex_count += 1
                    outfile.write('\n')
            
            # case material: texture field.
            else:
                tex = material.texture
                if tex is not None:
                    id = 'Texture' + str(tex_count).zfill(2)
                    textures[material.mat_id] = id
                
                    outfile.write('Texture "' + id + '" "spectrum" ')
                
                    if tex.tex_type == 'bitmap':
                        outfile.write('"imagemap" ')
                    else:
                        if tex.tex_type in mtpbrt.textureType:
                            tex_type = mtpbrt.textureType[tex.tex_type]
                            outfile.write('"' + tex_type + '" ')
                
                    for param in tex.params:
                        if param.name == 'filename':
                            outfile.write('"string filename" [ "' + param.value + '" ] ')
                        elif param.name == 'filterType':
                            if param.value == 'ewa':
                                outfile.write('"bool trilinear" [ "false" ] ')
                            else:
                                outfile.write('"bool trilinear" [ "true" ] ')
                        else:
                            # search the dictionary
                            p = pbrt_writeParams(shape.params, mtpbrt.textureParam)
                            outfile.write(p + '\n')
        

                    tex_count += 1
                    outfile.write('\n')


        # named material declaration
        for material in scene.materials:
            if isinstance(material, directives.BumpMap):
                outfile.write('MakeNamedMaterial "' + material.adapter.mat_id + '" ')
            
                outfile.write('\n')
            elif isinstance(material, directives.AdapterMaterial):
                outfile.write('MakeNamedMaterial "' + material.mat_id + '" ')

                outfile.write('\n')
            else:
                outfile.write('MakeNamedMaterial "' + material.mat_id + '" ')
                    
                outfile.write('\n')
                    
                    
        currentRefMaterial = ''
        for shape in scene.shapes:
            if shape.emitter is not None:
                if shape.emitter.type == 'area':
                    outfile.write('AttributeBegin\n')
                        
                    outfile.write('\tAreaLightSource "diffuse" ')
                    p = pbrt_writeParams(shape.emitter.params, mtpbrt.emitterParam)
                    outfile.write(p + '\n')
                        
                    shapeString = pbrt_shapeString(shape, 1)
                    outfile.write(shapeString + '\n')
                        
                    ref = shape.getReferenceMaterial()
                        
                    if not ref == '':
                        if ref != currentRefMaterial:
                            outfile.write('\tNamedMaterial "' + ref + '"\n')
                            outfile.write(shapeString)
                        else:
                            outfile.write(shapeString)
                        
                    outfile.write('AttributeEnd\n')
                        
                else:
                    
                    
            else:
                # if shape has ref material, then make reference
                shapeString = pbrt_shapeString(shape,0)
                
                ref = shape.getReferenceMaterial()
                        
                if not ref == '':
                    if ref != currentRefMaterial:
                        outfile.write('NamedMaterial "' + ref + '"\n')
                        outfile.write(shapeString)
                    else:
                        outfile.write(shapeString)
                    
                

        # end scene description
        outfile.write('WorldEnd\n')


def main():
    scene = mit.read_from_xml('/Users/luiza.hagemann/Development/pbr_scene_converter/test_files/mitsuba/staircase.xml')
    toPBRT(scene)

if  __name__ =='__main__': main()











